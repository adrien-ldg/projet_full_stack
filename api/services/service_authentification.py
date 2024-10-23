from fastapi import HTTPException, status, Response, Cookie
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from models import post
from .hashing import Hash
from . import auth_token


def login(r: OAuth2PasswordRequestForm, authentication: str, db: Session):
    if authentication:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session déja active. L'utilisateur est pas connecté.",
        )

    user = db.query(post.User).filter(post.User.email == r.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not Hash.verify(user.password, r.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")
    
    access_token = auth_token.create_access_token(
        data={"sub": user.email}
    )
    content = {"message": "Création cookie d'authentification"}
    response = JSONResponse(content=content)
    response.set_cookie(key="authentication", value=access_token, httponly=True, secure=True, samesite="strict", max_age=3600*12)
    return response


def logout(response: Response, authentication: str):
    if not authentication:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Aucune session active. L'utilisateur n'est pas connecté.",
        )

    try:
        response.delete_cookie(key="authentication")
        return {"message": "Cookie d'authentification supprimé."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
