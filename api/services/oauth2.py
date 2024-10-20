from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from . import auth_token
from shemas.shema import User
from models.db import get_db
from models import post
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def get_user(db: Session, email: str):
    user = db.query(post.User).filter(post.User.email == email).first()
    return {c.name: getattr(user, c.name) for c in user.__table__.columns}


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data =  auth_token.verify_Token(token, credentials_exception)

    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return User.model_validate(user)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user





    