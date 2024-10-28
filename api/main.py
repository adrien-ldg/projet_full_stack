from fastapi import FastAPI, Depends, Request, status, HTTPException
from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi.responses import HTMLResponse, RedirectResponse
from routers import router_film, router_cast, router_user, router_authentification
from models.database import engine, BaseSQL
from services.oauth2 import get_current_active_user
from shemas.shema import User, FilmOut, UserIn
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from services.service_film import get_all_films
from services import service_authentification
from models.db import get_db
from models import post  # Ajouter l'import de post
from services.hashing import Hash  # Ajouter l'import de Hash
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

# Route pour servir la page d'accueil HTML, avec redirection si non connecté
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    token = request.cookies.get("authentication")
    if not token:
        return RedirectResponse(url="/login")

    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

# Route pour servir la page de connexion
@app.get("/login", response_class=HTMLResponse)
async def login_page():
    with open("static/login.html") as f:
        return HTMLResponse(content=f.read())

# Route pour créer un nouvel utilisateur (inscription)
@app.post("/register/")
async def register(user: UserIn, db: Session = Depends(get_db)):
    existing_user = db.query(post.User).filter(post.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email déjà utilisé")
    
    new_user = post.User(
        email=user.email,
        password=Hash.bcrypt(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "Utilisateur créé avec succès"}

# Route pour afficher la version de l'application (protégée par authentification)
@app.get("/version")
async def get_version(current_user: User = Depends(get_current_active_user)):
    return {"app": "V1"}

# Route pour récupérer et retourner une liste de films
@app.get("/api/films", response_model=List[FilmOut])
async def get_films(db: Session = Depends(get_db)):
    films = get_all_films(limit=10, db=db)
    
    # Convertir chaque film en objet Pydantic FilmOut
    films_out = [FilmOut.from_orm(film) for film in films]
    return films_out
