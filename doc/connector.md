The `OmeroClient` class provides methods to interact with OMERO server via OMERO Python Gateway (BlitzGateway). It allows the user to authenticate, connect, disconnect and interact with images, projects, and datasets stored on OMERO server. The class constructor initializes the connection with OMERO server using the user's provided credentials, and allows the user to change the password as required.

- `__init__(self, username, host, port=4064)` initializes an instance of the `OmeroClient` class. The method takes the following parameters:
  
  - `username`: str - the user's OMERO username.
  - `host`: str - the OMERO server hostname.
  - `port`: int - the OMERO server port (default 4064).
  
  Upon initialization, this method creates a connection to the OMERO server, and sets up a signal handler to close the connection in case of an error. It also prints a warning message to remind the user to explicitly close the connection when they are done with the client.

- `show_user_summary(self)` retrieves the user details (id, name, full name) from the OMERO server and prints them to the console.

- `set_omero_group(self, group_id)` switches the session to a different group specified by `group_id`.

- `get_image_cursor(self, image_id)` retrieves an image object from the OMERO server based on the provided image id.

- `show_img_info(self, image_obj)` prints the image name, description, id, group id, size X, size Y, size Z, size C, and size T to the console.

- `get_image_thumbnail(self, image_obj, factor=100)` retrieves a thumbnail image from the OMERO server based on the provided image object, and returns a PIL Image object. The `factor` parameter is an integer value that determines the size of the thumbnail image, with a default value of 100.

- `get_image_jpg_region(self, image_obj, x: int, y: int, size: tuple) -> Image` retrieves a JPEG-encoded image region from the OMERO server based on the provided image object, and returns a PIL Image object. The `x` and `y` parameters are integers that represent the coordinates of the top-left corner of the image region to be retrieved, while the `size` parameter is a tuple that specifies the width and height of the region to be retrieved.

- `post_image(self, image_array: np.ndarray, image_name: str, dataset_id: int) -> int` uploads an image to the OMERO server using the provided `image_array`, `image_name`, and `dataset_id`. The `image_array` parameter must be a 5-dimensional numpy array, with dimensions Z, C, and T. The method returns the ID of the uploaded image.

- `create_project(self, project_name: str, description: Optional[str] = None) -> int` creates a new project with the provided `project_name` and `description` parameters, and returns the ID of the new project.

- `list_projects(self)` retrieves a list of all projects available to the current user on the OMERO server, and prints them to the console.

- `create_dataset(self, dataset_name: str, project_id: Optional[int] = None, description: Optional[str] = None, across_groups: Optional[bool] = True) -> int` creates a new dataset with the provided `dataset_name`, `

- `polygon_to_shape(polygon, z=0, t=0, c=0, text=None)` converts a 2D numpy array polygon into an omero polygon shape. The polygon shape will be positioned in the stack according to the specified z, c, and t coordinates. If text is provided, it will be set as the text value of the shape.

- `register_shape_to_roi(image, polygon, roi=None, z=0, t=0, c=0, text=None)`adds a polygon shape to an omero ROI associated with a given image. If roi is not provided, it creates a new ROI and links it to the image. The polygon is provided as a 2D numpy array and the position of the ROI within the stack is determined by the z, t, and c parameters. If text is provided, it will be set as the text value of the polygon shape. The method returns the saved ROI object.

- `add_metadata()` adds key-value pairs to an OMERO object such as a Project, Dataset, or Image. The `object_name` parameter specifies the type of object to which metadata is being added. The `object_id` parameter specifies the ID of the object to which the metadata is being added. The `key_value_data` parameter is a dictionary of key-value pairs to be added as metadata. 

- `add_file_metadata()` adds a file as metadata to an OMERO object such as a Project, Dataset, or Image. The `object_name` parameter specifies the type of object to which metadata is being added. The `object_id` parameter specifies the ID of the object to which the metadata is being added. The `namespace` parameter specifies the namespace to which the file belongs. The `filename` parameter specifies the path to the file to be added as metadata. 

- `delete_metadata()` deletes metadata from an OMERO object such as a Project, Dataset, or Image. The `object_name` parameter specifies the type of object from which metadata is being deleted. The `object_id` parameter specifies the ID of the object from which the metadata is being deleted. The `namespace` parameter specifies the namespace to which the metadata belongs. If `namespace` is `None`, all metadata associated with the object will be deleted. 

- `close()` closes the connection to the OMERO server. 

- `print_obj()` is a helper method used to display information about OMERO objects. It takes an OMERO object as input and prints out its class, ID, name, and owner.

- `__del__()` and `__exit__()` are special methods that are called when the `OmeroConnect` object is deleted or exited from a `with` statement. They call the `close()` method to close the connection to the OMERO server.