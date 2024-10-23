from fastapi import APIRouter, Depends, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from shemas.shema import User
from sqlalchemy.orm import Session
from models.db import get_db
from services import service_authentification


router = APIRouter(tags=["login/logout"])


#oui
@router.post("/login/", status_code=status.HTTP_202_ACCEPTED)
async def login(r: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), authentication: Annotated[str, Cookie()] = None):
    return service_authentification.login(r, authentication, db)

#oui
@router.post("/logout/", status_code=status.HTTP_202_ACCEPTED)
async def logout(r: Response, authentication: Annotated[str, Cookie()] = None):
    return service_authentification.logout(r, authentication)