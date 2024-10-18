from fastapi import APIRouter, status, Depends
from services import service_film
from sqlalchemy.orm import Session
from typing import List
from shemas.shema import FilmIn, FilmOut, CastIn
from models.db import get_db

router = APIRouter(prefix="/films", tags=["films"])


#non
@router.post("/", status_code=status.HTTP_201_CREATED , response_model=FilmOut)
async def create_film(c: List[CastIn], db: Session = Depends(get_db), r: FilmIn = Depends()):
        return service_film.create_film(r, c, db)
    

#oui
@router.get("/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=FilmOut)
async def get_one_films(title: str, db: Session = Depends(get_db)):
    return service_film.get_one_films(title, db)


#oui
@router.get("/", status_code=status.HTTP_202_ACCEPTED , response_model=List[FilmOut])
async def get_all_films(db: Session = Depends(get_db), limit: int = 10):
    return service_film.get_all_films(limit, db)
    

#non
@router.put("/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=FilmOut)
async def update_films(title: str, c: List[CastIn], db: Session = Depends(get_db), r:FilmIn = Depends()):
    return service_film.update_films(title, r, c, db)
    

#non
@router.delete("/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=FilmIn)
async def delete_films(title: str, db: Session = Depends(get_db)):
    return service_film.delete_films(title, db)



#oui
@router.get("/byrank/", status_code=status.HTTP_202_ACCEPTED , response_model=List[FilmOut])
async def get_film_by_rank(lr: int, hr: int, db: Session = Depends(get_db)):
    return service_film.get_film_by_rank(lr, hr, db)