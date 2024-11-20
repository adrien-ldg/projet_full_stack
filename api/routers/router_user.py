from fastapi import APIRouter, Depends, status, Body, Request
from sqlalchemy.orm import Session
from models.db import get_db
from shemas.shema import UserIn, User
from services import service_user
from services.oauth2 import get_current_active_user


router = APIRouter(prefix="/user", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(request : Request , r: UserIn = Body(...), db: Session = Depends(get_db)):
    body = await request.body()
    print("Reçu :", body.decode("utf-8"))  # Log les données brutes reçues

    return service_user.create_user(r, db)


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user