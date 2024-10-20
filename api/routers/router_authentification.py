from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from shemas.shema import Token
from sqlalchemy.orm import Session
from models.db import get_db
from services import service_authentification


router = APIRouter(prefix="/login", tags=["login"])

@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def login(r: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return service_authentification.login(r, db)