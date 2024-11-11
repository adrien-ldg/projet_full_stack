from fastapi import APIRouter, status, Depends, Query, Request
from fastapi.responses import HTMLResponse
from services import service_film, service_cast
from sqlalchemy.orm import Session
from typing import List, Annotated
from shemas.shema import FilmIn, FilmOut, CastIn, User
from models.db import get_db
from services.oauth2 import get_current_active_user

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


"""
#oui
@router.get("/{title}", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
async def get_one_films(title: str, request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    # Récupérer le film depuis le service
    film = service_film.get_one_films(title, db)
    
    # Si le film n'est pas trouvé, renvoyer une erreur 404
    if not film:
        return HTMLResponse(content="Film non trouvé", status_code=status.HTTP_404_NOT_FOUND)
    
    # Convertir l'objet film en dictionnaire
    film_dict = film.__dict__
    
    # Supprimer la clé `_sa_instance_state` générée par SQLAlchemy, qui n'est pas nécessaire dans le template
    film_dict.pop('_sa_instance_state', None)

    # Passer le dictionnaire film au template
    templates = request.app.state.templates
    return templates.TemplateResponse("one_film.html", {"request": request, "film": film_dict})

"""

#oui
@router.get("/", status_code=status.HTTP_202_ACCEPTED, response_class=HTMLResponse)
async def get_all_films(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), limit: int = 200):
    templates = request.app.state.templates

    films = service_film.get_all_films(limit, db)

    film_out_list = [FilmOut.model_validate(film) for film in films]

    print(film_out_list[0])

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
@router.get("/filter/", status_code=status.HTTP_202_ACCEPTED , response_model=List[FilmOut])
async def get_film_by_filter(lgross: int, hgross: int, lbudget: int, hbudget: int, ltime: int, htime: int, lyear: int, hyear: int, distributor: Annotated[str, Query()] = None, mpaa: Annotated[str, Query()] = None, genres: Annotated[List[str], Query()] = None, casts: Annotated[List[str], Query()] =  None, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_film.get_film_by_filter(lgross, hgross, distributor, lbudget, hbudget, mpaa, genres, ltime, htime, lyear, hyear, casts, db)