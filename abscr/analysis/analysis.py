import numpy as np
from PIL import Image
from shapely import measurement
import matplotlib.pyplot as plt


def calc_convexity(poly):
    return poly.convex_hull.length / poly.length


def calc_solidity(poly):
    return poly.area / poly.convex_hull.area


def calc_roundness(poly):
    return (4*np.pi * poly.area) / (poly.convex_hull.length**2)
