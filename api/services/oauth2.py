from fastapi import Depends, HTTPException, status, Cookie
from typing import Annotated
from . import auth_token
from shemas.shema import User
from models.db import get_db
from models import post
from sqlalchemy.orm import Session

def get_user(db: Session, email: str):
    user = db.query(post.User).filter(post.User.email == email).first()
    return {c.name: getattr(user, c.name) for c in user.__table__.columns}


def get_current_user(db: Session = Depends(get_db), authentication: Annotated[str, Cookie()] = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Utilisateur non authentifié",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if authentication:
        token_data = auth_token.verify_Token(authentication, credentials_exception)
    else:
        raise credentials_exception

    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return User.model_validate(user)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user





    