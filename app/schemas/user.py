from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr | None
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr | None
    is_active: bool
    created_at: datetime
    refresh_token: str | None
    access_token: str | None

    class Config:
        from_attributes = True