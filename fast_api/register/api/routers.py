from .models import post
from .models.db import get_db
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from .shema import Register, RegisterIn

from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=Register)
async def create(db: Session = Depends(get_db), r: RegisterIn = Depends()):
    record = db.query(post.Register).filter(post.Register.name == r.name).first()
    if record:
        raise HTTPException(status_code=409, detail="Already exists")
    
    try:

        new_post = post.Register(
            name = r.name,
            date_created = datetime.utcnow()
        )

        db.add(new_post)

        db.commit()

        db.refresh(new_post)

        return new_post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/register/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Register)
async def get_one(id: UUID, db: Session = Depends(get_db)):
    record = db.query(post.Register).filter(post.Register.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found") 
    return record


@router.get('/register/', status_code=status.HTTP_202_ACCEPTED, response_model=List[Register])
async def get_all(db: Session = Depends(get_db), limit: int = 10):
    posts = db.query(post.Register).filter().limit(limit).all()
    return posts


@router.put("/register/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Register)
async def update(id: UUID, db: Session = Depends(get_db), r: RegisterIn = Depends()):
    record = db.query(post.Register).filter(post.Register.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        
    record.name = r.name
    record.date_created = datetime.utcnow()

    db.commit()
    db.refresh(record)

    return record


@router.delete("/register/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Register)
async def delete(id: UUID, db: Session = Depends(get_db)):
    existing_record = db.query(post.Register).filter(post.Register.id == id).first()
    
    if not existing_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    db.delete(existing_record)
    db.commit()
    return existing_record