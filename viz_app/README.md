This code is a Bokeh-based Python script that generates a scatter plot with linked histograms on both axes. The script uses an image file and an outline file, and calculates certain properties of the shapes defined by the outlines. 

```
cd viz_app/

bokeh serve app.py
```

The `load_image` function takes the filename of an image, loads the image, compresses it, and returns it as a `PIL.Image` object. 

The `load_outlines` function takes the filename of an outline file, reads the file, and returns a list of strings representing the outlines.

The `polygons_from_outlines` function takes a list of outline strings, converts them to arrays of x,y coordinates, and appends them to a list of polygons, which is returned.

The `get_polygons` function takes an outline filename, calls `load_outlines` and `polygons_from_outlines`, and returns the list of polygons.

The `create_df` function takes a list of polygons, calculates certain properties of each polygon, and returns them as a `pandas.DataFrame`.

The `create_data_table` function takes a `pandas.DataFrame`, creates a `bokeh.models.ColumnDataSource` from it, and returns a `bokeh.models.DataTable` that displays the data.

The `im_2_b64` function takes a `PIL.Image` object, encodes it as a base64 string, and returns the string.