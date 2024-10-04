from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .database import BaseSQL

class Register(BaseSQL):
    __tablename__ = "register"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    name =  Column(String(500))
    date_created = Column(DateTime())