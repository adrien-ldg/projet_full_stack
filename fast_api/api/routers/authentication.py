from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from shema import Token
from sqlalchemy.orm import Session
from models.db import get_db
from models import post
from hashing import Hash
import auth_token


authentification_router = APIRouter(prefix="/login", tags=["login"])

@authentification_router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def login(r: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(post.User).filter(post.User.email == r.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    if not Hash.verify(user.password, r.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid password")
    
    access_token = auth_token.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}