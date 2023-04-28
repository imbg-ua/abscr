This module provides functions for calculating different measures of shape properties of a polygon. These shape properties are important in many areas of computer vision, image processing, and machine learning. The module includes the following functions:

- `calc_convexity` calculates the convexity of a polygon by dividing the length of its convex hull by its perimeter.
- `calc_solidity` calculates the solidity of a polygon by dividing its area by the area of its convex hull.
- `calc_roundness` calculates the roundness of a polygon by dividing 4 times pi times its area by the square of its convex hull perimeter. 

The functions take a shapely Polygon object as input and return a float value as output. The module requires numpy, PIL, shapely, and matplotlib.pyplot libraries.