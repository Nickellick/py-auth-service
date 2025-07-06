from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr]
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: UUID
    username: str
    email: Optional[EmailStr]
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True