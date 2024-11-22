from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY, BIGINT
from sqlalchemy.orm import relationship
from .database import BaseSQL

class Film(BaseSQL):
    __tablename__ = "films"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    rank = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    gross = Column(BIGINT, nullable=True)
    year = Column(Integer, nullable=False)
    summary = Column(String(1000), default="")
    image = Column(String(500), default="")
    distributor = Column(String(200), default="")
    budget = Column(BIGINT, nullable=True)
    MPAA = Column(String(100), default="pg")
    genres = Column(ARRAY(String), nullable=True)
    time = Column(Integer, nullable=False)
    release_date = Column(DateTime, nullable=False)

    cast = relationship("Cast", back_populates="film")
    


class Cast(BaseSQL):
    __tablename__ = "casts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(200), nullable=False)
    role = Column(String(200), nullable=False)
    character_name = Column(String(200), nullable=True)
    image =  Column(String(500), default="")
    film_id = Column(UUID(as_uuid=True), ForeignKey("films.id"))

    film = relationship("Film", back_populates="cast")


class User(BaseSQL):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(500))
    email = Column(String(500))
    password = Column(String(500))
    disabled = Column(Boolean)
