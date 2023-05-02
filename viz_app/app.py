''' Present a scatter plot with linked histograms on both axes.

Use the ``bokeh serve`` command to run the example by executing:

    bokeh serve selection_histogram.py

at your command prompt. Then navigate to the URL

    http://localhost:5006/selection_histogram

in your browser.

'''
from bokeh.models import LinearColorMapper, ColorBar
from bokeh.transform import transform
from bokeh.plotting import figure
from bokeh.palettes import Blues9
from scipy.stats import gaussian_kde
import base64
from io import BytesIO
import numpy as np

from bokeh.layouts import gridplot, row, column
from bokeh.models import (BoxSelectTool, LassoSelectTool, DataTable, NumberEditor, SelectEditor,
                          IntEditor, NumberFormatter, SelectEditor,
                          StringEditor, StringFormatter, Select, HoverTool,
                          ColumnDataSource, TableColumn, Dropdown, Button)
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Patches, Plot
from bokeh.models import CustomJS
from bokeh.plotting import curdoc, figure
from PIL import Image
import os
from bokeh.sampledata.autompg2 import autompg2 as mpg
from abscr.analysis.analysis import calc_convexity, calc_roundness, calc_solidity
from shapely import Polygon, centroid
from shapely.geometry import Point
from shapely.plotting import plot_polygon, plot_points
from shapely import measurement
import pandas as pd

DATA_DIR = 'data'


def load_image(img_filename):
    image = Image.open(os.path.join(DATA_DIR, img_filename)).convert('L')
    image.save("data/image-file-compressed.jpg",
               "JPEG",
               optimize=True,
               quality=10)

    return Image.open('data/image-file-compressed.jpg')


def load_outlines(filename):
    with open(os.path.join(DATA_DIR, filename)) as f:
        outlines = f.readlines()
    return outlines


def handle_image(attr, old, new):
    image = load_image(new)
    return image


def polygons_from_outlines(outlines):
    polygons = []
    for o in outlines:
        if len(o) < 2:
            continue
        coords_flat = np.fromstring(o, sep=',').astype(int)
        # make pairs x, y
        polyg = np.array([np.array(x)
                         for x in zip(coords_flat[::2], coords_flat[1::2])])
        polygons.append(polyg)
    return polygons


def handle_outlines(attr, old, new):
    outlines = load_outlines(new)
    polygons = polygons_from_outlines(outlines)
    return


# dropdown_outlines.on_change('value', handle_outlines)
# END DROPDWON


# PATCHES
def get_polygons(filename):
    outlines = load_outlines(filename)
    polygons = polygons_from_outlines(outlines)
    return polygons


outlines_filename = '020_Buccal_05.04.2022_small_cp_outlines(2).txt'
polygs = get_polygons(outlines_filename)


def create_df(polygons):
    diams = []
    convs = []
    solds = []
    rounds = []
    xs = []
    ys = []

    for i, poly in enumerate(polygons):  # np.expand_dims(polygons, axis=0)
        cur_poly = Polygon(poly)
        mbr = measurement.minimum_bounding_radius(cur_poly)
        cntr = centroid(cur_poly)

        xs.append(cntr.x)
        ys.append(cntr.y)
        diams.append(mbr*2)

        convexity = calc_convexity(cur_poly)
        solidity = calc_solidity(cur_poly)
        roundness = calc_roundness(cur_poly)

        convs.append(convexity)
        solds.append(solidity)
        rounds.append(roundness)

    data = [xs, ys, diams, convs, solds, rounds]
    df = pd.DataFrame(data).T
    df.columns = ['x', 'y', 'diameter', 'convexity', 'solidity', 'roundness']
    df['cell_class'] = None
    return df.round(2)


def create_data_table(dataframe):
    source = ColumnDataSource(dataframe)
    cols = ['cell_class', 'x', 'y', 'diameter',
            'convexity', 'solidity', 'roundness']
    table_cols = []
    for c in cols:
        table_cols.append(TableColumn(field=c))
    data_table = DataTable(source=source,
                           editable=True,
                           selectable=True,
                           sortable=True,
                           width=400,
                           columns=table_cols,
                           index_position=None)
    return (data_table, source)


df = create_df(polygs)
data_table, source = create_data_table(df)


def update_labels():
    pass


table_button = Button(label="Press to set", button_type="success")
table_button.on_click(update_labels)


def im_2_b64(image):
    buff = BytesIO()
    image.save(buff, format="png")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


TOOLS = "pan, wheel_zoom, box_select, lasso_select, reset"

#  IMAGE
img_filename = '020_Buccal_05.04.2022_small.jpeg'
img = load_image(img_filename)

# TODO: flip?
img = Image.fromarray(np.flipud(img))

img_arr = np.array(img)
# print(img_arr.shape)
img_b64 = im_2_b64(img)

url = 'data:image/png;base64,' + img_b64.decode('utf-8')

# create the scatter plot
aspect_ratio = 500/1100
p = figure(tools=TOOLS,
           width=930,
           height=int(930*aspect_ratio),
           min_border=0,
           min_border_left=0,
           #    sizing_mode = 'fixed',
           toolbar_location="above",
           title="")
p.background_fill_color = "#fafafa"
p.select(BoxSelectTool).select_every_mousemove = False
p.select(LassoSelectTool).select_every_mousemove = False


r = p.circle(x="x", y="y", fill_color="#396285",
             size=10, alpha=0.0, source=source, )


p.image_url(url=[url],
            x=0,
            y=0,
            w=img_arr.shape[1],
            h=img_arr.shape[0],
            anchor="bottom_left",
            global_alpha=0.8)

# create the horizontal histogram
hhist, hedges = np.histogram(df.x.values, bins=32)
hzeros = np.zeros(len(hedges)-1)
hmax = max(hhist)*1.1


# KDE


def kde(x, y, N):
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:N*1j, ymin:ymax:N*1j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    kernel = gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    return X, Y, Z


x, y, z = kde(df.x, df.y, 300)

pkde = figure(toolbar_location=None, width=p.width, height=200, x_range=p.x_range,
              min_border=0, min_border_left=0)
pkde.grid.level = "overlay"
pkde.grid.grid_line_color = "black"
pkde.grid.grid_line_alpha = 0.05

palette = Blues9[::-1]
levels = np.linspace(np.min(z), np.max(z), 10)
pkde.contour(x, y, z, levels[1:], fill_color=palette, line_color=palette)


LINE_ARGS = dict(color="#3A5785", line_color=None)

ph = figure(toolbar_location=None, width=p.width, height=100, x_range=p.x_range,
            y_range=(-hmax, hmax), min_border=0, min_border_left=0, y_axis_location="right")
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4
ph.background_fill_color = "#fafafa"

ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:],
        top=hhist, color="white", line_color="#3A5785")
hh1 = ph.quad(
    bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
hh2 = ph.quad(
    bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)


# DROPDWON
image_formats = ['.png', 'tiff', '.jpg', 'jpeg']
menu_image = [x for x in os.listdir('data') if x[-4:] in image_formats]

dropdown_image = Select(value=menu_image[0], options=menu_image)

dropdown_image.on_change('value', handle_image)


menu_outlines = [x for x in os.listdir('data') if x[-3:] == 'txt']
menu_outlines.insert(0, '')
dropdown_outlines = Select(value=menu_outlines[0], options=menu_outlines)
# dropdown_outlines.js_on_event("menu_item_click", CustomJS(
#     code="console.log('dropdown_outlines: ' + this.item, this.toString())"))


xs = []
ys = []
for polygs in polygs:
    xs.append([x[0] for x in polygs])
    ys.append([x[1] for x in polygs])

poly_source = ColumnDataSource(dict(
    xs=xs,
    ys=ys,
    diameter=df['diameter']
)
)

color_mapper = LinearColorMapper(palette="Viridis256",
                                 low=df.diameter.min(),
                                 high=df.diameter.max())

color_bar = ColorBar(color_mapper=color_mapper,
                     #  label_standoff = 14,
                     #  location = (0,0),
                     title='Diameter')
p.add_layout(color_bar, 'right')

p.patches(xs='xs',
          ys='ys',
          fill_color={'field': 'diameter', 'transform': color_mapper},
          source=poly_source,
          alpha=0.75,
          )
# Add the HoverTool to the figure
tooltips = [
    ('diameter', '@diameter'), ('id', '@index')
]
p.add_tools(HoverTool(tooltips=tooltips))

layout = gridplot([[row(dropdown_image, dropdown_outlines)],
                   [column(p, pkde, ph), column(data_table, table_button)],]
                  )

curdoc().add_root(layout)
curdoc().title = "Annotation viz app"


def update(attr, old, new):
    inds = new
    if len(inds) == 0 or len(inds) == len(df.x.values):
        hhist1, hhist2 = hzeros, hzeros
    else:
        neg_inds = np.ones_like(df.x.values, dtype=np.bool)
        neg_inds[inds] = False
        hhist1, _ = np.histogram(df.x.values[inds], bins=hedges)

        hhist2, _ = np.histogram(df.x.values[neg_inds], bins=hedges)
    hh1.data_source.data["top"] = hhist1
    hh2.data_source.data["top"] = -hhist2


r.data_source.selected.on_change('indices', update)
