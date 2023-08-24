import cv2
import math
import numpy as np
import pandas as pd

def read_outlines_from_txt(outlines_file):
    res = []
    with open(outlines_file) as f:
        outlines = f.readlines()
        for o in outlines:
            coords_flat = np.fromstring(o, sep=',').astype(int)
            res.append(coords_flat)
    return np.array(res, dtype=object)

def moving_average(array, num_avg):
    '''
    Smoothes numerical 1D array applying moving average methods.

        Parameters:
            array (np.ndarray): array of numerical data
            num_avg (int): number of following elements to calculate average (moving average parameter)

        Returns:
            res (np.ndarray): array of smoothed data
    '''
    res = []
    # array_extended = array + array[:num_avg - 1]
    array_extended = np.append(array, array[:num_avg - 1])
    for i in range(len(array)):
        res.append(sum(array_extended[i:i + num_avg]) / num_avg)
    return np.array(res)

def scale_outlines(outlines_file, factor):
    '''
    Scales outlines read from a .txt file with a given factor.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            factor (int): scaling factor

        Returns:
            outlines_scaled (list): list of scaled outlines
    '''
    outlines_scaled = []

    with open(outlines_file) as f:
        outlines = f.readlines()
        for o in outlines:
            coords_flat = np.fromstring(o, sep=',').astype(int)
            outlines_scaled.append(coords_flat * factor)

    outlines_scaled = np.array(outlines_scaled, dtype=object)
    return outlines_scaled

def scale_outlines_from_array(outlines, factor):
    '''
    Scales outlines read from a list with a given factor.

        Parameters:
            outlines (list-like): outlines
            factor (int): scaling factor

        Returns:
            outlines_scaled (list): list of scaled outlines
    '''
    outlines_scaled = []

    for coords_flat in outlines:
        outlines_scaled.append(coords_flat * factor)

    outlines_scaled = np.array(outlines_scaled, dtype=object)
    return outlines_scaled

def save_outlines_to_txt(outlines, savename):
    '''
    Saves array of outlines into a file

        Parameters:
            outlines (list-like): outlines
            savename (str): file name
    '''
    with open(savename, 'w') as f:
        for o in outlines:
            f.write(','.join(map(lambda x: str(x), o)) + '\n')

def smooth_outlines_moving_avg(outlines_file, num_avg=5):
    '''
    Smoothes outlines stored in a .txt file using moving average technique.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            num_avg (int): moving average parameter

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    smoothed = []
    with open(outlines_file, 'r') as f:
        outlines = f.readlines()
        for o in outlines:
            coords_flat = np.fromstring(o, sep=',').astype(int)
            coords_flat[::2] = moving_average(coords_flat[::2], num_avg)
            coords_flat[1::2] = moving_average(coords_flat[1::2], num_avg)
            smoothed.append(coords_flat)
    return smoothed

def smooth_outlines_moving_avg_from_array(outlines, num_avg=5):
    '''
    Smoothes outlines stored in list using moving average technique.

        Parameters:
            outlines (list-like): outlines
            num_avg (int): moving average parameter

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    smoothed = []
    for coords_flat in outlines:
        coords_flat[::2] = moving_average(coords_flat[::2], num_avg)
        coords_flat[1::2] = moving_average(coords_flat[1::2], num_avg)
        smoothed.append(coords_flat)
    return smoothed

def iterative_scaling_moving_avg(outlines_file, num_avg=5, factor=8, scale_step=2):
    '''
    Iteratively scales outlines read from a .txt file by alternating smoothing and scaling steps.
    Provided parameters factor and scale_step must satisfy the requirement that log_{scale_step}(factor) is an integer.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            num_avg (int): moving average parameter
            factor (int): total scaling factor
            scale_step (int): size of a single scaling step

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    num_iter = math.log(factor, scale_step)
    assert num_iter % 1 == .0, 'Iterative scaling requires an integer number of scaling steps'

    smoothed = smooth_outlines_moving_avg(outlines_file, num_avg)
    for i in range(1, int(num_iter) + 1):
        scaled = scale_outlines_from_array(smoothed, 2)
        smoothed = smooth_outlines_moving_avg_from_array(scaled)

    return smoothed

def iterative_scaling_moving_avg_from_array(outlines, num_avg=5, factor=8, scale_step=2):
    '''
    Iteratively scales outlines stored in a list by alternating smoothing and scaling steps.
    Provided parameters factor and scale_step must satisfy the requirement that log_{scale_step}(factor) is an integer.

        Parameters:
            outlines_file (str): path to a file containing mask outlines
            num_avg (int): moving average parameter
            factor (int): total scaling factor
            scale_step (int): size of a single scaling step

        Returns:
            smoothed (list): list of smoothed outlines
    '''
    num_iter = math.log(factor, scale_step)
    print(num_iter % 1)
    assert num_iter % 1 == .0, 'Iterative scaling requires an integer number of scaling steps'

    smoothed = smooth_outlines_moving_avg_from_array(outlines, num_avg)
    for i in range(1, int(num_iter) + 1):
        scaled = scale_outlines_from_array(smoothed, 2)
        smoothed = smooth_outlines_moving_avg_from_array(scaled)

    return smoothed

def add_masks_to_img(image, polygons, color=(55, 55, 255), alpha=0.3, line_color=(0, 0, 0), thickness=1):
    '''
    Adds masks to an input image in the form of filled polygons, and returns a new image with the masks overlaid onto the
    original image with transparency. The function also adds outlines to the polygons with a specified line color and
    thickness.

    Parameters:
    - image: An input image to which the masks will be added. The image should be read using `cv2.imread()` and be in
      the format of a numpy array with shape (height, width, channels) and color channels in BGR order.
    - polygons: A list of polygons in the form of numpy arrays with shape (N, 1, 2), where N is the number of points in
      the polygon. The polygons should be in the format [[x1, y1], [x2, y2], ..., [xn, yn]].
    - color: An optional tuple of three integers representing the BGR color value of the filled polygons. The default
      value is (55, 55, 255), which corresponds to a shade of red.
    - alpha: An optional float between 0 and 1 representing the transparency of the filled polygons. The default value
      is 0.3.
    - line_color: An optional tuple of three integers representing the BGR color value of the polygon outlines. The
      default value is (0, 0, 0), which corresponds to black.
    - thickness: An optional integer representing the thickness of the polygon outlines in pixels. The default value is 1.

    Returns:
    - image_new: A new image with the filled polygons overlaid onto the original input image with transparency, and the
      polygon outlines added. The image has the same shape and data type as the input image.
    '''
    img_copy = image.copy()
    filled = np.array(img_copy)
    filled = cv2.fillPoly(filled, pts=polygons, color=color)
    image_new = cv2.addWeighted(filled, alpha, img_copy, 1 - alpha, 0)
    image_new = cv2.polylines(image_new, pts = polygons, color=line_color, thickness=thickness, isClosed=True)
    return image_new

def make_polygons_from_outlines(outlines_file):
    polygons = []
    with open(outlines_file) as f:
        outlines = f.readlines()
        for o in outlines:
            coords_flat = np.fromstring(o, sep=',').astype(int)
            polyg = np.array([np.array(x) for x in zip(coords_flat[::2], coords_flat[1::2])])
            polygons.append(polyg)
    return polygons

def make_polygons_from_outlines_array(outlines):
    polygons = []
    for coords_flat in outlines:
        polyg = np.array([np.array(x) for x in zip(coords_flat[::2], coords_flat[1::2])])
        polygons.append(polyg)
    return polygons

def filter_outlines(min_w, max_w, min_h, max_h, outlines, indent_left=0, indent_top=0):
    '''
    Filters out outlines that don't fall into the specified rectangle region and shifts their coordinates
    relative to this region. Useful for plotting masks on a small region of a larger image.

    If the original WSI was cropped before the segmentation step, the resulting masks (outlines) have
    coordinates relative to the cropped image. To plot such masks over the region from the original image,
    one can pass indentation values (indent_left and indent_top) which represent the numbers of pixels
    cut off from the original image during the preprocessing step.

        Parameters:
            min_w (int): left coordinate of the bounding box
            max_w (int): right coordinate of the bounding box
            min_h (int): upper coordinate of the bounding box
            max_h (int): lower coordinate of the bounding box
            outlines (list-like): list of outlines
            indent_left (int, default 0): left side indentation
            indent_top (int, default 0): top side indentation

        Returns:
            res (list): list of outlines
    '''
    res = []
    for o in outlines:
        belongs_to_region = True
        for x in zip(o[::2], o[1::2]):
            if not min_w < (x[0] + indent_left) < max_w or not min_h < (x[1] + indent_top) < max_h:
                belongs_to_region = False
                break

        if belongs_to_region:
            cur_outline = np.empty_like(o)
            cur_outline[::2] = o[::2] - min_w + indent_left
            cur_outline[1::2] = o[1::2] - min_h + indent_top
            res.append(cur_outline)
    return res

def outlines_to_wkt_polygons(outlines_file, object_type='Epithelial cell'):
    polygons = make_polygons_from_outlines(outlines_file)
    dat = []

    for i, polygon in enumerate(polygons):
        polygon_wkt = 'Polygon (('
        first_polygon_wkt = ''
        for j, point in enumerate(polygon):
            if j == 0:
                first_polygon_wkt = f"{point[0]} {point[1]}"
            polygon_wkt += f"{point[0]} {point[1]}, "
        polygon_wkt += f'{first_polygon_wkt}))'
        dat.append([polygon_wkt, object_type, i + 1])

    dat = pd.DataFrame(dat, columns=['polygon', 'name', 'object'])
    return dat
