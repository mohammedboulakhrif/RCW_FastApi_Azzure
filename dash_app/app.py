import dash
from dash import html, dcc
import requests

# Crée l'app Dash
app = dash.Dash(__name__, requests_pathname_prefix='/dashboard/')

# Récupération des Infos météo via ton API FastAPI
try:
    response = requests.get("http://localhost:8001/info")
    if response.status_code == 200:
        Info = response.json()
    else:
        Info = {
            "date": "N/A",
            "time": "N/A",
            "weather": {
                "city": "Erreur API",
                "temperature": "N/A",
                "description": "Erreur API"
            }
        }
except Exception as e:
    Info = {
        "date": "N/A",
        "time": "N/A",
        "weather": {
            "city": "Erreur",
            "temperature": "N/A",
            "description": str(e)
        }
    }

# Layout de l'app Dash
app.layout = html.Div([
    html.Div([
        html.A('Home', href='/'),
    ], style={'marginTop': '20px'}),

    html.H2("Informations météo"),
    html.P(f"Ville : {Info['weather']['city']}"),
    html.P(f"Température : {Info['weather']['temperature']} °C"),
    html.P(f"Description : {Info['weather']['description']}"),
    html.P(f"Date : {Info['date']}"),
    html.P(f"Heure : {Info['time']}"),

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
