from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime

class Register(BaseModel):
    id: UUID
    name: str
    date_created: datetime

    class Config:
        orm_mode = True

class RegisterIn(BaseModel):
    name: str = Field(...)