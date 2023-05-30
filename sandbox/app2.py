from dash import Dash, dcc, html
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([dcc.Markdown('''
    $E^2=m^2c^4+p^2c^2$
    ''', mathjax=True),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
