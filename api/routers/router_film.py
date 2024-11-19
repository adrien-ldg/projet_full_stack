from fastapi import APIRouter, status, Depends, Query, Request
from fastapi.responses import HTMLResponse
from services import service_film, service_cast
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional
from shemas.shema import FilmIn, FilmOut, CastIn, User
from models.db import get_db
from services.oauth2 import get_current_active_user
from fastapi.templating import Jinja2Templates
router = APIRouter(prefix="/films", tags=["films"])


#non
@router.post("/", status_code=status.HTTP_201_CREATED , response_model=FilmOut)
async def create_film(cast: List[CastIn], db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), r: FilmIn = Depends()):
        return service_film.create_film(r, cast, db)
    

@router.get("/{title}", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
async def get_one_films(title: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Récupérer le film depuis le service
    film = service_film.get_one_films(title, db)
    
    if not film:
        return HTMLResponse(content="Film non trouvé", status_code=status.HTTP_404_NOT_FOUND)
    # Convertir l'objet film en dictionnaire
    film_dict = film.__dict__
    
    
    # Récupérer le casting
    cast = service_cast.get_cast_one_film(title, db)

    # Passer film et cast au template sans conversion en dictionnaire
    templates = request.app.state.templates
    return templates.TemplateResponse("one_film.html", {"request": request, "film": film_dict, "cast": cast})




#oui
@router.get("/", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
async def get_all_films(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), limit: int = 200):
    templates = request.app.state.templates

    films = service_film.get_all_films(limit, db)

    film_out_list = [FilmOut.model_validate(film) for film in films]


    return templates.TemplateResponse(name="all_films.html", request=request, context={"films": film_out_list})
    

#non
@router.put("/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=FilmOut)
async def update_films(title: str, cast: List[CastIn], db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), r:FilmIn = Depends()):
    return service_film.update_films(title, r, cast, db)
    

#non
@router.delete("/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=FilmIn)
async def delete_films(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_film.delete_films(title, db)



#oui
@router.get("/byrank/", status_code=status.HTTP_202_ACCEPTED , response_model=List[FilmOut])
async def get_film_by_rank(lr: int, hr: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_film.get_film_by_rank(lr, hr, db)

#oui
templates = Jinja2Templates(directory="templates")
@router.get("/filter/", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
async def get_film_by_filter(
    request: Request,
    lgross: Optional[str] = Query(None),  # Min gross
    hgross: Optional[str] = Query(None),  # Max gross
    distributor: Optional[str] = Query(None),  # Distributor
    lbudget: Optional[str] = Query(None),  # Min budget
    hbudget: Optional[str] = Query(None),  # Max budget
    mpaa: Optional[str] = Query(None),  # MPAA rating
    genres: Optional[List[str]] = Query(None),  # Selected genres
    ltime: Optional[str] = Query(None),  # Min runtime
    htime: Optional[str] = Query(None),  # Max runtime
    lyear: Optional[str] = Query(None),  # Min year
    hyear: Optional[str] = Query(None),  # Max year
    casts: Optional[List[str]] = Query(None),  # Selected cast members
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Convertir les valeurs numériques en entiers ou infini si absentes
    lgross = int(lgross) if lgross and lgross.isdigit() else float('-inf')
    hgross = int(hgross) if hgross and hgross.isdigit() else float('inf')
    lbudget = int(lbudget) if lbudget and lbudget.isdigit() else float('-inf')
    hbudget = int(hbudget) if hbudget and hbudget.isdigit() else float('inf')
    ltime = int(ltime) if ltime and ltime.isdigit() else float('-inf')
    htime = int(htime) if htime and htime.isdigit() else float('inf')
    lyear = int(lyear) if lyear and lyear.isdigit() else float('-inf')
    hyear = int(hyear) if hyear and hyear.isdigit() else float('inf')

    
    # Obtenir tous les films
    films = service_film.get_all_films(limit=200, db=db)
    if not any([lgross, hgross, lbudget, hbudget, ltime, htime, lyear, hyear, distributor, mpaa, genres, casts]):
        templates = request.app.state.templates
        return templates.TemplateResponse("all_films.html", {"request": request, "films": films})
    # Appliquer les filtres
    filtered_films = []

    for film in films:
        # Vérifier les genres
        """film_genres = (
            film.genres
            if isinstance(film.genres, list)
            else film.genres.strip("[]").replace("'", "").split(", ")
        )"""
        if genres and not all(selected_genre in film.genres for selected_genre in genres):
            continue

        # Vérifier les critères numériques
        if not (lgross <= film.gross <= hgross):
            continue
        if not (lbudget <= film.budget <= hbudget):
            continue
        if not (ltime <= film.time <= htime):
            continue
        if not (lyear <= film.year <= hyear):
            continue

        # Vérifier le distributeur
        if distributor and film.distributor == distributor:
            continue

        # Vérifier le MPAA rating
        if mpaa and film.MPAA == mpaa:
            continue

        # Vérifier les castings
        if casts:
            film_cast_names = [cast.name for cast in film.cast]
            if not any(selected_cast in film_cast_names for selected_cast in casts):
                continue


        # Si toutes les conditions sont respectées, ajouter le film à la liste filtrée
        filtered_films.append(film)

    # Retourner les films filtrés au template
    templates = request.app.state.templates
    return templates.TemplateResponse(
        "all_films.html",
        {"request": request, "films": filtered_films}
    )
    
    
    
@router.get("/distributors/", status_code=status.HTTP_200_OK)
async def get_unique_distributors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # Récupérer tous les films
    films = service_film.get_all_films(limit=200, db=db)
    # Extraire les distributeurs uniques
    distributors = {film.distributor for film in films if film.distributor}
    print(distributors)
    # Retourner une liste triée
    return sorted(distributors)