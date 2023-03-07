import numpy as np
import PIL
from tiffslide import TiffSlide
from abscr.segmentation import segmentor

EPITHELIAL_CELL_DIAMETER = 60 # epithelial cell diameter in micrometers

class Preprocessor:
    def __init__(self) -> None:
        pass

    def scale_image(self, image, factor, cell_diameter=None):
        if isinstance(image, TiffSlide):
            level = image.get_best_level_for_downsample(factor)
            if cell_diameter is not None:
                cell_diam_pixels_scaled = cell_diameter / factor
            else:
                cell_diameter = EPITHELIAL_CELL_DIAMETER
                cell_diam_pixels = cell_diameter / ((image.properties['tiffslide.mpp-x'] + image.properties['tiffslide.mpp-y']) / 2)
                cell_diam_pixels_scaled = cell_diam_pixels / image.properties[f'tiffslide.level[{level}].downsample']

            w, h = image.properties[f'tiffslide.level[{level}].width'], image.properties[f'tiffslide.level[{level}].height']
            return (image.read_region((0, 0), level, (w, h)), cell_diam_pixels_scaled)

        elif isinstance(image, np.ndarray):
            PIL_image = PIL.Image.fromarray(image)
            height, width = PIL_image.size[0] // factor, PIL_image.size[1] // factor

            if cell_diameter is None:
                cell_diameter = EPITHELIAL_CELL_DIAMETER

            cell_diam_scaled = cell_diameter / factor
            return (PIL_image.resize((height, width)), cell_diam_scaled)
        else:
            PIL_image = segmentor.Segmentor().check_image(image)
            height, width = PIL_image.size[0] // factor, PIL_image.size[1] // factor

            if cell_diameter is None:
                cell_diameter = EPITHELIAL_CELL_DIAMETER

            cell_diam_scaled = cell_diameter / factor
            return (PIL_image.resize((height, width)), cell_diam_scaled)


    def crop_image(self, image, left, upper, right, lower, level=None) -> 'PIL.Image':
        if isinstance(image, TiffSlide):
            if level is None:
                raise ValueError('When passing an image as TiffSlide object, the level must be specified.')
                return
            return image.read_region((left, upper), level, (right - left, lower - upper))
        elif isinstance(image, np.ndarray):
            PIL_image = PIL.Image.fromarray(image)
            return PIL_image.crop((left, upper, right, lower))
        else:
            PIL_image = segmentor.Segmentor().check_image(image)
            return PIL_image.crop((left, upper, right, lower))
