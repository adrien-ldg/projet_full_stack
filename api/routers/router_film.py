from fastapi import APIRouter, status, Depends, Query
from services import service_film
from sqlalchemy.orm import Session
from typing import List, Annotated
from shemas.shema import FilmIn, FilmOut, CastIn, User
from models.db import get_db
from services.oauth2 import get_current_active_user

router = APIRouter(prefix="/films", tags=["films"])


#non
@router.post("/", status_code=status.HTTP_201_CREATED , response_model=FilmOut)
async def create_film(c: List[CastIn], db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), r: FilmIn = Depends()):
        return service_film.create_film(r, c, db)
    

#oui
@router.get("/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=FilmOut)
async def get_one_films(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return service_film.get_one_films(title, db)


#oui
@router.get("/", status_code=status.HTTP_202_ACCEPTED , response_model=List[FilmOut])
async def get_all_films(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), limit: int = 10):
    return service_film.get_all_films(limit, db)
    

#non
@router.put("/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=FilmOut)
async def update_films(title: str, c: List[CastIn], db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user), r:FilmIn = Depends()):
    return service_film.update_films(title, r, c, db)
    

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