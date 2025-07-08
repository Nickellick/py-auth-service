from types import new_class

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/login", response_model=UserRead)
async def login(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
        result = await db.execute(select(User).where(User.username == user_in.username))
        if not (user := result.scalar()):
            raise HTTPException(status_code=404, detail="User not found")
        return user


@router.post("/register", response_model=UserRead)
async def register(user_in: UserLogin, request: Request, db: AsyncSession = Depends(get_db)) -> User:
    user_agent = request.headers.get("user-agent", "unknown")
    ip = request.client.host if request.client else "unknown"
    result = await db.execute(select(User).where(User.username == user_in.username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password)
    )
    # TODO Create token
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
