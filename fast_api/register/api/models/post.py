from uuid import uuid4
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import BaseSQL

class Register(BaseSQL):
    __tablename__ = "register"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name =  Column(String(500))
    date_created = Column(DateTime())
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    creator = relationship("User", back_populates="register")


class User(BaseSQL):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name = Column(String(500))
    email = Column(String(500))
    password = Column(String(500))
    disabled = Column(Boolean)

    register = relationship("Register", back_populates="creator")