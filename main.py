import sys
import os

# Ajout du répertoire parent au path système
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.templating import Jinja2Templates
import uvicorn
from dash_app.app import app as app_dash # Assure-toi que dash_app/app.py existe
import requests

app = FastAPI()

# Répertoires corrigés (templates et static sont dans fastapi_app/)
base_dir = os.path.dirname(__file__)
templates_dir = os.path.join(base_dir, "fastapi_app", "templates")
static_dir = os.path.join(base_dir, "fastapi_app", "static")

# Montage des fichiers statiques et des templates
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# Utilisateur de test
user = {"admin": "123"}


# External_API_URL='http://localhost:8001/info'
External_API_URL='https://weatherappi-hebaffd2bef7c6dj.canadaeast-01.azurewebsites.net/info'

def get_external_info():
    try:
        response=requests.get(External_API_URL)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except Exception as e:
        print("error from weather api :",e)
        return{
            "date":"N/A",
            "time": "N/A",
            "weather": {
                "city": "unknown",
                "temperature": "N/A",
                "description": "Unable to get data"             
            }
        }

# Route d’accueil
@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    info=get_external_info()
    return templates.TemplateResponse("home.html", { #ici ou on a passer les info a home.html
        "request": request,
        "Info":info,
        "message": "Bienvenue sur ma page home de l’API FastAPI"
    })

# Page de login (GET)
@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": None
    })

# Traitement du formulaire de login (POST)
@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in user and user[username] == password:
        return RedirectResponse(url="/dashboard", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Identifiants incorrects"
        })

# Intégration de l'application Dash
app.mount("/dashboard", WSGIMiddleware(app_dash.server))


# Lancer avec : uvicorn main1:app --reload
