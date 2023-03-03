import dash
import dash_canvas
from dash import dash_table

import pandas as pd
from dash import html

from dash.dependencies import Input, Output, State
from dash_canvas.utils import parse_jsonstring_rectangle
from dash_canvas.utils import io_utils
from PIL import Image
import numpy as np


# filename = 'https://raw.githubusercontent.com/plotly/datasets/master/mitochondria.jpg'
filename = '020_Buccal_05.04.2022_small.jpeg'
img = Image.open(filename)
img_string = io_utils.array_to_data_url(np.asarray(img))

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

list_columns = ['width', 'height', 'left', 'top', 'class']
list_labels = ['epithelial', 'immune', 'debris', 'empty']

columns = [{'name': i, "id": i} for i in list_columns]
columns[-1]['presentation'] = 'dropdown'

label_classes = [{'label': i, 'value': i} for i in list_labels]


app.layout = html.Div([
    html.Div([
        html.H3('Label images with bounding boxes', style={'color': '#444444'}),
        dash_canvas.DashCanvas(
            id='canvas',
            width=800,
            tool='rectangle',
            image_content=img_string,
            lineWidth=2,
            lineColor='rgba(0, 255, 0, 0.5)',
            # filename=filename,
            hide_buttons=['pencil', 'line', 'pan'],
            goButtonTitle='Label'
        ),
    ]),
    html.Div([
        dash_table.DataTable(
            fill_width=True,
            id='table',
            columns=columns,
            editable=True,
            dropdown={
                'class': {
                    'options': label_classes
                }
            }

        ),
    ]),
    html.Div('Save annotations:'),
        html.Button('As txt (TBD)', id="get-txt", style={'pointer-events': 'none'}),
        html.Button('As JSON (TBD)', id="get-json", style={'pointer-events': 'none'}),
])


@app.callback(Output('table', 'data'), [Input('canvas', 'json_data')])
def show_string(json_data):
    box_coordinates = parse_jsonstring_rectangle(json_data)
    df = pd.DataFrame(box_coordinates, columns=list_columns[:-1])
    df['class'] = 'empty'
    return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
