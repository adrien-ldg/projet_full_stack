from models import post
from models.db import get_db
from oaut2 import get_current_user
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from shema import Register, RegisterIn, ShowRegister, User
from sqlalchemy.orm import Session

register_router = APIRouter(prefix="/register", tags=["register"])


@register_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowRegister)
async def create(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), r: RegisterIn = Depends()):
    record = db.query(post.Register).filter(post.Register.name == r.name).first()
    if record:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exists")
    
    try:
        print(current_user)
        new_post = post.Register(
            name = r.name,
            date_created = datetime.utcnow(),
            user_id = current_user.id 
        )

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@register_router.get("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowRegister)
async def get_one(id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    record = db.query(post.Register).filter(post.Register.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found") 
    return record


@register_router.get('/', status_code=status.HTTP_202_ACCEPTED, response_model=List[Register])
async def get_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), limit: int = 10):
    posts = db.query(post.Register).filter().limit(limit).all()
    return posts


@register_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ShowRegister)
async def update(id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), r: RegisterIn = Depends()):
    record = db.query(post.Register).filter(post.Register.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
        
    record.name = r.name
    record.date_created = datetime.utcnow()

    db.commit()
    db.refresh(record)

    return record


@register_router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Register)
async def delete(id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_record = db.query(post.Register).filter(post.Register.id == id).first()
    
    if not existing_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    db.delete(existing_record)
    db.commit()
    return existing_record