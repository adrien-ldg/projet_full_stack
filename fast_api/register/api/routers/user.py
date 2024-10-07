from fastapi import APIRouter, Depends, HTTPException, status
from ..shema import UserIn, ShowUser, User
from sqlalchemy.orm import Session
from ..models.db import get_db
from ..models import post
from ..hashing import Hash
from uuid import UUID
from ..oaut2 import get_current_active_user


user_router = APIRouter(prefix="/user", tags=["users"])


@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(r: UserIn, db: Session = Depends(get_db)):
    try:
        record = db.query(post.User).filter(post.User.name == r.name).first()
        if record:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already exists")
        
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
    

@user_router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user