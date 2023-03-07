# https://omero-guides.readthedocs.io/en/latest/python/docs/gettingstarted.html

import getpass
from typing import Optional
import omero.clients
from omero.gateway import BlitzGateway
import getpass
from PIL import Image
import io
import os
import logging
from signal import SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM, signal
import ezomero
import numpy as np

logging.basicConfig(level=logging.WARNING)


class OmeroClient:
    def __init__(self, username, host, port=4064):
        self.username = username
        self.__password = None
        self.host = host
        self.port = port
        self._open_connect()

        for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
            signal(sig, self.close)

        logging.warn(
            'Close the connection explicitly. Use OmeroClientInstance.close() after you done with omero client.')

    def _open_connect(self):
        n_attempt = 0
        connected = False
        while not connected:
            if self.__password is None:
                password = getpass.getpass(
                    prompt='Enter your password' if n_attempt == 0 else 'Try again, wrong password')
            else:
                password = self.__password

            conn = BlitzGateway(self.username,
                                password,
                                host=self.host,
                                secure=True)
            conn.connect()
            n_attempt += 1
            connected = conn.isConnected()
            if not connected:
                conn.close()

        self.__set_password(password)
        logging.info('Connected.')
        conn.c.enableKeepAlive(120)
        self.conn = conn

    def _keep_connection(self):
        logging.info('Checking connection status')
        if self.conn:
            if self.conn.isConnected():
                return
        self._open_connect()
        logging.info('Successfully reconnected')

    def __set_password(self, password):
        self.__password = password

    def show_user_summary(self):
        self._keep_connection()

        user = self.conn.getUser()
        print("Current user:")
        print("   ID:", user.getId())
        print("   Username:", user.getName())
        print("   Full Name:", user.getFullName())

    def set_omero_group(self, group_id):
        # https://forum.image.sc/t/omero-py-group-switching/65162/7
        # ‘cross-group’ querying, use ‘-1’
        # Will query across all my groups
        # ----
        # allows saving changes to the object etc.
        # group_id = image_object.getDetails().group.id.val
        # self.conn.SERVICE_OPTS.setOmeroGroup(group_id)
        self._keep_connection()
        self.conn.SERVICE_OPTS.setOmeroGroup(group_id)

    def get_image_cursor(self, image_id):
        self._keep_connection()
        return self.conn.getObject('Image', image_id)

    def show_img_info(self, image_obj):
        self._keep_connection()

        print(image_obj.getName())
        print(image_obj.getDescription())
        print('Image_id:', image_obj.getId())
        print('Group_id:', image_obj.getDetails().group.id.val)
        print(" X:", image_obj.getSizeX())
        print(" Y:", image_obj.getSizeY())
        print(" Z:", image_obj.getSizeZ())
        print(" C:", image_obj.getSizeC())
        print(" T:", image_obj.getSizeT())

    def get_image_thumbnail(self, image_obj, factor=100):
        self._keep_connection()

        w, h = image_obj.getSizeX(), image_obj.getSizeY()
        thumbnail = image_obj.getThumbnail(size=(w/factor, h/factor))
        result = Image.open(io.BytesIO(thumbnail))
        result.filename = image_obj.getName()
        return result

    def get_image_jpg_region(self, image_obj, x: int, y: int, size: tuple) -> Image:
        self._keep_connection()

        w, h = size
        # TODO: z, t
        z, t = 0, 0
        im_jpg_bytes = image_obj.renderJpegRegion(z, t, x, y, w, h)
        result = Image.open(io.BytesIO(im_jpg_bytes))
        filename, ext = os.path.splitext(image_obj.getName())
        result.filename = f'{filename}_{x}_{y}_{w}x{h}{ext}'
        return result

    def post_image(self, image_array: np.ndarray, image_name: str, dataset_id: int) -> int:
        '''
        Parameters
        ----------
        image_array : array like image input. Image must be 5-dim, with Z, C, T dims.
        dataset_id : id of the dataset where the image will be posted.
        '''

        self._keep_connection()
        im_id = ezomero.post_image(
            conn=self.conn, image=image_array, image_name=image_name, dataset_id=dataset_id)
        return im_id

    def create_project(self, project_name: str, description: Optional[str] = None) -> int:
        return ezomero.post_project(self.conn, project_name, description)

    def list_projects(self):
        self._keep_connection()
        projects = self.conn.listProjects()      # may include other users' data
        for p in projects:
            print('-',
                  p.getName(),
                  '\n ',
                  "Owner: ",
                  p.getDetails().getOwner().getFullName())

    def create_dataset(self, dataset_name: str, project_id: Optional[int] = None, description: Optional[str] = None, across_groups: Optional[bool] = True) -> int:
        self._keep_connection()
        did = ezomero.post_dataset(conn=self.conn, dataset_name=dataset_name, project_id=project_id, description=description, across_groups=across_groups)
        return did

    @staticmethod
    def polygon_to_shape(polygon, z=0, t=0, c=0, text=None):
        """Creates an omero roi shape from an ndarray polygon instance
        Parameters
        ----------
        polygon : np.ndarray with shape (N, 2)
            where N is the number of points in the polygon
        z, c, t : ints
            the Z, C and T position of the shape in the stack
        """

        shape = omero.model.PolygonI()
        shape.theZ = omero.rtypes.rint(z)
        shape.theT = omero.rtypes.rint(t)
        shape.theC = omero.rtypes.rint(c)
        if text and len(text) > 0:
            shape.setTextValue(omero.rtypes.rstring(text))
        shape.points = omero.rtypes.rstring(
            ", ".join((f"{int(p[0])},{int(p[1])}" for p in polygon)))
        return shape

    def register_shape_to_roi(self, image, polygon, roi=None, z=0, t=0, c=0, text=None):
        """Adds a polygon shape to an omero ROI. If no roi is provided,
        creates it first.
        Parameters
        ----------
        image : omero Image object
        polygon : np.ndarray of shape (N, 2)
        conn : connection to the omero db
        roi : omero ROI, default None
        if it is None, a new ROI will be created
        z, t, c : position of the ROI in the stack (defaults to 0)
        Returns
        -------
        roi: the roi
        """

        self._keep_connection()
        updateService = self.conn.getUpdateService()
        if roi is None:
            # create an ROI, link it to Image
            roi = omero.model.RoiI()
            # use the omero.model.ImageI that underlies the 'image' wrapper
            roi.setImage(image._obj)
        
        # TODO: make possible to input polygon as omero.model.PolygonI() as well, not only as an np.ndarray
        shape = self.polygon_to_shape(polygon, z=z, t=t, c=c, text=text)
        roi.addShape(shape)
        # Save the ROI (saves any linked shapes too)
        return updateService.saveAndReturnObject(roi)

    def close(self, *args):
        if self.conn and self.conn.isConnected():
            self.conn.close()
            logging.info('Connection is closed.')

    @staticmethod
    def print_obj(obj, indent=0):
        """
        Helper method to display info about OMERO objects.
        Not all objects will have a "name" or owner field.
        """
        print("""%s%s:%s  Name:"%s" (owner=%s)""" % (
            " " * indent,
            obj.OMERO_CLASS,
            obj.getId(),
            obj.getName(),
            obj.getOwnerOmeName()))

    def __del__(self):
        try:
            self.close()
        except Exception as e:
            print(e)

    def __exit__(self, type, value, traceback):
        try:
            self.close()
        except Exception as e:
            print(e)
