from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import post
from shemas.shema import UserIn
from .hashing import Hash



def create_user(r: UserIn, db: Session):
    try:
        record = db.query(post.User).filter(post.User.name == r.name).first()
        if record:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        
        record = db.query(post.User).filter(post.User.email == r.email).first()
        if record:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
        
        new_user = post.User(
            name= r.name,
            email= r.email,
            password= Hash.bcrypt(r.password),
            disabled=False
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))