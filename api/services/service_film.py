from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from models import post
from shemas.shema import FilmIn, CastIn
from typing import List
from datetime import datetime

def create_film(r: FilmIn, c: List[CastIn], db: Session):
    record = db.query(post.Film).filter(post.Film.title == r.title).first()
    if record:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Film already exists")
    
    try:
        new_film = post.Film(
            rank = r.rank,
            title = r.title,
            gross = r.gross,
            year = r.year,
            summary = r.summary,
            image = r.image,
            distributor = r.distributor,
            budget = r.budget,
            MPAA = r.MPAA,
            genres = r.genres,
            time = r.time,
            release_date = r.release_date
        )


        db.add(new_film)
        db.commit()

        new_casts = [
            post.Cast(
                name=cast.name,
                role=cast.role,
                character_name=cast.character_name,
                image=cast.image,
                film_id=new_film.id
            )
            for cast in c
        ]
        db.add_all(new_casts)
        db.commit()
        db.refresh(new_film)

        return new_film
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_one_films(title: str, db: Session):
    record = db.query(post.Film).filter(post.Film.title == title).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not Found") 
    return record


def get_all_films(limit: int, db: Session):
    try:
        posts = db.query(post.Film).filter().limit(limit).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def update_films(title: str, r:FilmIn, c: List[CastIn], db: Session):
    record = db.query(post.Film).filter(post.Film.title == title).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")
    
    try:

        record.rank = r.rank
        record.title = r.title
        record.gross = r.gross
        record.year = r.year
        record.summary = r.summary
        record.image = r.image
        record.distributor = r.distributor
        record.budget = r.budget
        record.MPAA = r.MPAA
        record.genres = r.genres
        record.time = r.time
        record.release_date = r.release_date
        

        for cast in c:
            db.query(post.Cast).filter(post.Cast.film_id == record.id, post.Cast.name == cast.name).delete()

        new_casts = [
            post.Cast(
                name=cast.name,
                role=cast.role,
                character_name=cast.character_name,
                image=cast.image,
                film_id=record.id
            )
            for cast in c
        ]
        
        db.add_all(new_casts)
        db.commit()
        db.refresh(record)

        return record
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def delete_films(title: str, db: Session):
    existing_record = db.query(post.Film).filter(post.Film.title == title).first()
    
    if not existing_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")

    try:
        db.query(post.Cast).filter(post.Cast.film_id == existing_record.id).delete()

        db.delete(existing_record)
        db.commit()

        return existing_record

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def get_film_by_rank(lr: int, hr: int, db: Session):
    
    record = db.query(post.Film).filter(post.Film.rank >= lr, post.Film.rank <= hr).all()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Films not Found") 
    return record

def get_film_by_filter(lgross: int, hgross: int, distributor: str, lbudget: int, hbudget: int, mpaa: str, genres: List[str], ltime: int, htime: int, lrelease_date: datetime, hrelease_date: datetime, casts: List[str], db: Session):
    try:
        query = db.query(post.Film).filter(post.Film.gross >= lgross,
                                            post.Film.gross <= hgross,
                                            post.Film.budget >= lbudget,
                                            post.Film.budget <= hbudget,
                                            post.Film.time >= ltime,
                                            post.Film.time <= htime,
                                            post.Film.release_date >= lrelease_date,
                                            post.Film.release_date <= hrelease_date)
        if distributor:
            query = query.filter(post.Film.distributor == distributor)
        if mpaa:
            query = query.filter(post.Film.MPAA == mpaa)
        if genres:
            query = query.filter(post.Film.genres.in_(genres))
        if casts:
            query = query.filter(post.Cast.name.in_(casts))
        
        record = query.all()

        if not record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Films not Found") 
        return record
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
