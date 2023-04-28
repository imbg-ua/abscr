This module provides functions for calculating different measures of shape properties of a polygon. These shape properties are important in many areas of computer vision, image processing, and machine learning. The module includes the following functions:

- `calc_convexity` calculates the convexity of a polygon by dividing the length of its convex hull by its perimeter.
- `calc_solidity` calculates the solidity of a polygon by dividing its area by the area of its convex hull.
- `calc_roundness` calculates the roundness of a polygon by dividing 4 times pi times its area by the square of its convex hull perimeter. 

The functions take a shapely Polygon object as input and return a float value as output. The module requires numpy, PIL, shapely, and matplotlib.pyplot libraries.

| Method | Input | Output | Description |
| --- | --- | --- | --- |
| `calc_convexity(poly)` | `shapely.geometry.Polygon` | `float` | Takes a polygon object as input and returns the convexity of the polygon. The convexity is defined as the length of the polygon's convex hull divided by the length of the polygon. |
| `calc_solidity(poly)` | `shapely.geometry.Polygon` | `float` | Takes a polygon object as input and returns the solidity of the polygon. The solidity is defined as the area of the polygon divided by the area of its convex hull. |
| `calc_roundness(poly)` | `shapely.geometry.Polygon` | `float` | Takes a polygon object as input and returns the roundness of the polygon. The roundness is defined as 4π times the area of the polygon divided by the square of its perimeter (i.e., the length of its convex hull). |

<b>`calc_convexity(poly)`</b>
This function takes a `shapely.geometry.Polygon` object as input and returns the convexity of the polygon. The convexity is defined as the length of the polygon's convex hull divided by the length of the polygon. A perfectly convex polygon has a convexity of 1, while a more concave polygon has a convexity less than 1.

<b>`calc_solidity(poly)`</b>
This function takes a `shapely.geometry.Polygon` object as input and returns the solidity of the polygon. The solidity is defined as the area of the polygon divided by the area of its convex hull. A perfectly solid polygon has a solidity of 1, while a more irregular polygon has a solidity less than 1.

<b>`calc_roundness(poly)`</b>
This function takes a `shapely.geometry.Polygon` object as input and returns the roundness of the polygon. The roundness is defined as 4π times the area of the polygon divided by the square of its perimeter (i.e., the length of its convex hull). A perfectly round polygon has a roundness of 1, while a more elongated polygon has a roundness less than 1. Note that this definition of roundness is sometimes also called the "circularity" or "compactness" of the polygon.