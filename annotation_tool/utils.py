# helper functions

import numpy as np

def get_polygons_from_outlines(outlines_txt):
    polygons = []
    for o in outlines_txt:
        coords_flat = np.fromstring(o, sep=',').astype(int)
        # make pairs x, y
        polyg = np.array([np.array(x) for x in zip(coords_flat[::2], coords_flat[1::2])])
        polygons.append(polyg)
    return polygons
