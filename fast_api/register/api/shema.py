from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from uuid import UUID


class RegisterIn(BaseModel):
    name: str = Field(...)

    class Config:
        from_attributes = True


class Register(BaseModel):
    name: str
    date_created: datetime

    class Config:
        from_attributes = True


class UserIn(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    id: UUID
    name: str
    email: str
    password: str
    disabled: bool | None = None


class ShowUser(BaseModel):
    name: str
    email: str
    register: List[Register] = []

    class Config:
        from_attributes = True

class ShowRegister(BaseModel):
    name: str
    date_created: datetime
    creator: ShowUser

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None