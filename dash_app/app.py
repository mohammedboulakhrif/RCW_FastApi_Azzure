import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__, requests_pathname_prefix='/dashboard/')

app.layout = html.Div([
    html.Div([
        html.A('Home', href='/'),
    ], style={'marginTop': '20px'}),

    html.H2("Informations météo"),
    html.P(id='city'),
    html.P(id='temperature'),
    html.P(id='description'),
    html.P(id='date'),
    html.P(id='time'),

    dcc.Graph(
        id='exmpl_1',
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [6, 9, 4], "type": "bar", "name": "Example 1"},
                {"x": [7, 2, 5], "y": [3, 7, 1], "type": "bar", "name": "Example 2"}
            ]
        }
    ),

    # Interval pour recharger toutes les 60 secondes (par exemple)
    dcc.Interval(id='interval', interval=60*1000, n_intervals=0)
])

@app.callback(
    Output('city', 'children'),
    Output('temperature', 'children'),
    Output('description', 'children'),
    Output('date', 'children'),
    Output('time', 'children'),
    Input('interval', 'n_intervals')
)
def update_weather(n):
    try:
        response = requests.get("https://weatherappi-hebaffd2bef7c6dj.canadaeast-01.azurewebsites.net/info")
        if response.status_code == 200:
            info = response.json()
        else:
            info = {
                "date": "N/A",
                "time": "N/A",
                "weather": {
                    "city": "Erreur API",
                    "temperature": "N/A",
                    "description": "Erreur API"
                }
            }
    except Exception as e:
        info = {
            "date": "N/A",
            "time": "N/A",
            "weather": {
                "city": "Erreur",
                "temperature": "N/A",
                "description": str(e)
            }
        }

    return (
        f"Ville : {info['weather']['city']}",
        f"Température : {info['weather']['temperature']} °C",
        f"Description : {info['weather']['description']}",
        f"Date : {info['date']}",
        f"Heure : {info['time']}"
    )
