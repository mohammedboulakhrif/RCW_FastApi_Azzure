import dash
from dash import html, dcc

app = dash.Dash(__name__, requests_pathname_prefix='/dashboard/')

app.layout = html.Div(children=[
    html.Div([
        html.A('Home', href='/'),
    ], style={'marginTop': '20px'}),

    dcc.Graph(
        id='exmpl_1',
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [6, 9, 4], "type": "bar", "name": "Example 1"},
                {"x": [7, 2, 5], "y": [3, 7, 1], "type": "bar", "name": "Example 2"}
            ]
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
