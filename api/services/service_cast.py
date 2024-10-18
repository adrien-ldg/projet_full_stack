from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import post
from uuid import UUID
from shemas.shema import CastIn


def create_cast(c: CastIn, film_id: UUID, db: Session):
    film = db.query(post.Film).filter(post.Film.id == film_id).first()
    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film doesn't exist")


    record = db.query(post.Cast).filter(post.Cast.name == c.name, post.Cast.film_id == film_id).first()
    if record:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cast already exists")
    
    try:
        new_cast = post.Cast(
            name = c.name,
            role = c.role,
            character_name = c.character_name,
            image = c.image,
            film_id = film_id
        )


        db.add(new_cast)
        db.commit()
        db.refresh(new_cast)

        return new_cast
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def get_one_cast(id: UUID, db: Session):
    record = db.query(post.Cast).filter(post.Cast.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cast not Found") 
    return record


def get_cast_one_film(title: str, db: Session):
    film = db.query(post.Film).filter(post.Film.title == title).first()

    if not film:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not found")

    record = db.query(post.Cast).filter(post.Cast.film_id == film.id).all()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Film not Found") 
    return record


def get_cast_one_name(name: str, db: Session):
    record = db.query(post.Cast).filter(post.Cast.name == name).all()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not Found") 
    return record


def get_all_cast(limit: int, db: Session,):
    try:
        posts = db.query(post.Cast).filter().limit(limit).all()
        return posts
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


def update_cast(id: UUID, film_id: UUID, c: CastIn, db: Session):
    record = db.query(post.Cast).filter(post.Cast.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cast not found")
    
    try:

        record.name = c.name
        record.role = c.role
        record.character_name = c.character_name
        record.image = c.image
        if film_id:
            record.film_id = film_id
        
        db.commit()
        db.refresh(record)

        return record
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def delete_cast(id: UUID, db: Session):
    existing_record = db.query(post.Cast).filter(post.Cast.id == id).first()
    
    if not existing_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cast not found")

    try:
        db.delete(existing_record)
        db.commit()

        return existing_record

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))