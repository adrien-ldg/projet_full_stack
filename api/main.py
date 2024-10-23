from fastapi import FastAPI, Depends
from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi.responses import HTMLResponse  # Importer pour retourner du HTML
from routers import router_film, router_cast, router_user, router_authentification
from models.database import engine, BaseSQL
from services.oauth2 import get_current_active_user
from shemas.shema import User, FilmOut
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from services.service_film import get_all_films  # Importation de la fonction du service
from models.db import get_db  # Fonction pour obtenir la session DB
from typing import List

async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

# Middleware pour Prometheus (monitoring)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

# Inclusion des différents routers
app.include_router(router_film.router)
app.include_router(router_cast.router)
app.include_router(router_user.router)
app.include_router(router_authentification.router)

# Monter le répertoire des fichiers statiques (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Route pour servir la page d'accueil HTML
@app.get("/", response_class=HTMLResponse)
async def read_index():
    # Retourner le fichier HTML index comme page d'accueil
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

# Route pour afficher la version de l'application (protégée par authentification)
@app.get("/version")
async def get_version(current_user: User = Depends(get_current_active_user)):
    return {"app": "V1"}
@app.get("/api/films", response_model=List[FilmOut])
async def get_films(db: Session = Depends(get_db)):
    films = get_all_films(limit=10, db=db)
    
    # Manuellement convertir chaque film en objet Pydantic
    films_out = [FilmOut.from_orm(film) for film in films]
    print(films_out)
    return films_out
