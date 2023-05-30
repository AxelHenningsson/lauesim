from dash import Dash, html, Input, Output, State, dcc, html
import plotly.express as px
import dash_daq as daq
import numpy as np
from lauesim import dct
from scipy.spatial.transform import Rotation
import dash_bootstrap_components as dbc


app = Dash(__name__)
np.random.seed(1)
my_dct_model = dct.model()
baserot = my_dct_model.sample.orientation[0].copy()

class state():
    def __init__(self):
        self.ANGLE  = 180
        self.MOSAIC = 0.5
        self.WORKING_DISTANCE = np.abs(my_dct_model.geometry.working_distance)
        self.ORIENTATION = 0
        self.AXIS_ID = 0

    def get_axis(self):
        axis = np.zeros((3,))
        axis[self.AXIS_ID] = 1
        return axis

appState = state()

def _get_frame_as_fig():

    my_dct_model.geometry.frame *= 0
    my_dct_model.collect()
    frame = my_dct_model.geometry.render()

    fig   = px.imshow(frame)
    fig.update_layout(
                hoverlabel={
                    "font": {"family": "monospace"},
                },
                template = "plotly_dark",
                font={"family": "monospace", "size": 18},
                margin={
                    "pad": 0,
                    "t": 0,
                    "r": 0,
                    "l": 0,
                    "b": 0,
                }
            )
    fig.update_layout({"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": 'rgba(0,0,0,0)'})
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(showlegend=False)
    return fig

def _get_rotated_frame(value):
    my_dct_model.sample.rotation_angle = np.radians(value)
    return _get_frame_as_fig()

def _get_mosaic_frame(value):
    N = my_dct_model.sample.points.shape[0]
    ang = np.random.normal(loc=0, scale=np.radians(value), size=(N,))
    unitvec = np.random.normal(loc=0, scale=1, size=(N,3))
    rotvec = ang.reshape(N,1) * unitvec / np.linalg.norm(unitvec, axis=1).reshape(N,1)
    Udiff = Rotation.from_rotvec(rotvec).as_matrix()
    my_dct_model.sample.orientation = np.array([U.dot(baserot) for U in Udiff])
    return _get_frame_as_fig()

def _get_orientation_shifted_frame(ang, axis):
    rotvec = axis*np.radians(ang)
    Udiff = Rotation.from_rotvec(rotvec).as_matrix()
    shiftedU = my_dct_model.sample.orientation.copy()
    for i in range(shiftedU.shape[0]):
        shiftedU[i] = Udiff.dot(shiftedU[i])
    my_dct_model.sample.orientation = shiftedU
    return _get_frame_as_fig()

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}
font = 'sans-serif'

rootLayout = html.Div([
        html.Br(),
        dcc.Markdown('''**DCT Diffraction Pattern From a Single alpha-Quartz Crystal**''',
                     style={'color': 'white', 'fontSize': 24, 'textAlign': 'center', 'font-family':font}),
        html.Br(),
        dcc.Graph(id="dct-image", figure=_get_rotated_frame(180)),
        html.Br(),
        dcc.Markdown('''**Sample Rotation Angle (degrees)**''', style={'color': 'white', 'fontSize': 18, 'font-family':font}),
        dcc.Slider(
            id='rotation-angle-slider',
            min=0,
            max=360,
            step=0.1,
            value=180,
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag',
            marks={
                0: {'label': '0'},
                90: {'label': '90'},
                180: {'label': '180'},
                270: {'label': '270'},
                360: {'label': '360'}
            },
        ),
        html.Br(),
        dcc.Markdown('''
        **Mosaicity; Standard Deviation of Gaussian Orientation Spread (degrees)**
        ''', style={'color': 'white', 'fontSize': 18, 'font-family':font}),
        dcc.Slider(
            id='mosaic-slider',
            min=0,
            max=5,
            step=0.01,
            value=0,
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag',
           marks={
                0: {'label': '0'},
                1: {'label': '1'},
                2: {'label': '2'},
                3: {'label': '3'},
                4: {'label': '4'},
                5: {'label': '5'},
            },
        ),
        html.Br(),
        dcc.Markdown('''
        **Orientation; Mean of Gaussian Orientation Spread (degrees)**
        ''', style={'color': 'white', 'fontSize': 18, 'font-family':font}),
        dcc.Slider(
            id='orientation-slider',
            min=0,
            max=15,
            step=0.01,
            value=appState.ORIENTATION,
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag',
           marks={
                0: {'label': '0'},
                3: {'label': '3'},
                6: {'label': '6'},
                9: {'label': '9'},
                12: {'label': '12'},
                15: {'label': '15'},
            },
        ),
        html.Br(),
        dcc.Markdown('''
        **Orientation Shift Axis (lab coordinates)**
        ''', style={'color': 'white', 'fontSize': 18, 'font-family':font}),
        dcc.RadioItems(options=[
            {
                "label": html.Div(['X-axis'], style={'color': 'Gold', 'font-size': 20}),
                "value": 'X-axis',
            },
            {
                "label": html.Div(['Y-axis'], style={'color': 'MediumTurqoise', 'font-size': 20}),
                "value":'Y-axis',
            },
            {
                "label": html.Div(['Z-axis'], style={'color': 'LightGreen', 'font-size': 20}),
                "value": 'Z-axis',
            },
            ],
            labelStyle={"display": "flex", "align-items": "center"},
            inline=True,
            id='axis-of-orientation-shift',
            value=['X-axis', 'Y-axis','Z-axis'][appState.AXIS_ID],
        ),
        html.Br(),
        dcc.Markdown('''
        **LAUE Focus Working Distance (mm)**
        ''', style={'color': 'white', 'fontSize': 18, 'font-family':font}),
        dcc.Slider(
            id='working-distance-slider',
            min=10,
            updatemode='drag',
            max=90,
            step=1,
            value=int(appState.WORKING_DISTANCE/1000.),
            tooltip={"placement": "bottom", "always_visible": True},
           marks={
                10: {'label': '10mm'},
                30: {'label': '30mm'},
                50: {'label': '50mm'},
                70: {'label': '70mm'},
                90: {'label': '90mm'},
            },
        ),
        html.Br(),
        html.Div([
            html.Br(),
            ]*50,    style={
        'backgroundColor':'#303030',
        "padding": "0px",
        "margin": "0px",
        "margin-left": 50,
        "margin-right": 50,
        "margin": 0}),
],    style={
        'backgroundColor':'#303030',
        "padding": "0px",
        "margin": "0px",
        "margin-left": 50,
        "margin-right": 50,
        "margin": 0})


app.layout = html.Div(id='dark-theme-components-1', children=[
        daq.DarkThemeProvider(theme=theme, children=rootLayout)
    ], style={
        'backgroundColor':'#303030',
        "padding": "0px",
        "margin": "0px",
        "margin-left": 0,
        "margin-right": 0,
        "margin": 0
    }, )


@app.callback(
        Output("dct-image", "figure"),
        Input("rotation-angle-slider", "value"),
        Input("mosaic-slider", "value"),
        Input("working-distance-slider", "value"),
        Input("orientation-slider-x", "value"),
        Input("orientation-slider-y", "value"),
        Input("orientation-slider-z", "value"),

)
def on_click(angle, mosaic, working_distance, orientation_x, orientation_y, orientation_z):
    print()
    if angle!=appState.ANGLE:
        appState.ANGLE = angle
        return _get_rotated_frame(angle)
    elif mosaic!=appState.MOSAIC:
        appState.MOSAIC = mosaic
        return _get_mosaic_frame(mosaic)
    elif 1000*working_distance!=appState.WORKING_DISTANCE:
        appState.WORKING_DISTANCE = working_distance*1000.
        my_dct_model.geometry.working_distance = working_distance*1000.
        return _get_frame_as_fig()
    elif orientation_x!=appState.ORIENTATION_X:
        shift = orientation_x-appState.ORIENTATION_X
        fig = _get_orientation_shifted_frame(shift, axis=np.array([1,0,0]))
        appState.ORIENTATION_X = orientation_x
        return fig
    elif orientation_y!=appState.ORIENTATION_Y:
        shift = orientation_y-appState.ORIENTATION_Y
        fig = _get_orientation_shifted_frame(shift, axis=np.array([0,1,0]))
        appState.ORIENTATION_Y = orientation_y
        return fig
    elif orientation_z!=appState.ORIENTATION_Z:
        shift = orientation_z-appState.ORIENTATION_Z
        fig = _get_orientation_shifted_frame(shift, axis=np.array([0,0,1]))
        appState.ORIENTATION_Z = orientation_z
        return fig
if __name__ == '__main__':
    app.run_server(debug=True)
