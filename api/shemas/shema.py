from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from datetime import datetime


class Film(BaseModel):
    id: UUID
    rank: int
    title: str
    gross: int
    year: int
    summary: str
    image: str
    distributor: str
    budget: int
    MPAA: str
    genres: List[str]
    time: int
    release_date: datetime

    class Config:
        from_attributes = True


class Cast(BaseModel):
    id: UUID
    name: str
    role: str
    character_name: Optional[str] = None 
    image: str
    film_id: UUID

    class Config:
        from_attributes = True


class FilmIn(BaseModel):
    rank: int
    title: str = Field(...)
    gross: int
    year: int
    summary: str = ""
    image: str = ""
    distributor: str = ""
    budget: int
    MPAA: str = "pg"
    genres: Optional[List[str]] = Field(default_factory=list)
    time: int
    release_date: datetime = datetime.utcnow()


class CastIn(BaseModel):
    name: str = Field(...)
    role: str = Field(...)
    character_name: str = ""
    image: str = ""

    class Config:
        from_attributes = True


class CastOut(BaseModel):
    name: str
    role: str
    character_name: Optional[str] = None
    image: str

    film: Film

    class Config:
        from_attributes = True


class FilmOut(BaseModel):
    rank: int
    title: str 
    gross: int
    year: int
    summary: str
    image: str
    distributor: str
    budget: Optional[int] = None
    MPAA: str
    genres: Optional[List[str]] = None
    time: int
    release_date: datetime

    cast: List[Cast] = []

    class Config:
        from_attributes = True


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class User(BaseModel):
    name: str
    email: str
    disabled: Optional[bool] = None

    class Config:
        from_attributes = True


class UserInDB(User):
    password: str


class Login(BaseModel):
    email: str
    password: str
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
