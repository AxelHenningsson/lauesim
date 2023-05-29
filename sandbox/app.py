from dash import Dash, html, Input, Output, State, dcc, html
import plotly.express as px
import dash_daq as daq
import numpy as np
from lauesim import dct
from scipy.spatial.transform import Rotation

app = Dash(__name__)
my_dct_model = dct.model()

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
    U = Rotation.random(N, random_state=int(np.round(value*1000)))
    my_dct_model.sample.orientation = U
    return _get_frame_as_fig()


theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

rootLayout = html.Div([
        html.Br(),
        dcc.Graph(id="dct-image", figure=_get_rotated_frame(180)),
        html.Br(),
        dcc.Slider(
            id='rotation-angle-slider',
            min=0, 
            max=360,
            step=1, 
            value=180,
            tooltip={"placement": "bottom", "always_visible": True},
            marks={
                0: {'label': '0°'},
                90: {'label': '90°'},
                180: {'label': '180°'},
                270: {'label': '270°'},
                360: {'label': '360°'}
            },
        ),
        dcc.Slider(
            id='mosaic-slider',
            min=0, 
            max=1,
            step=0.01, 
            value=0,
            tooltip={"placement": "bottom", "always_visible": True},
            marks=None,
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
)
def get_rotated_frame(value):
    return _get_rotated_frame(value)


@app.callback(
    Output("dct-image", "figure"),
    Input("mosaic-slider", "value"),
)
def get_mosaic_frame(value):
    print(value)
    return _get_mosaic_frame(value)

if __name__ == '__main__':
    app.run_server(debug=True)
