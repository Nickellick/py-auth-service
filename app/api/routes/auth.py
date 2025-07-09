from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.security import create_hash, verify_hash
from app.services.user import generate_jwt_for_user

router = APIRouter()

@router.post("/login", response_model=UserLogin)
async def login(user_in: UserCreate, request: Request, db: AsyncSession = Depends(get_db)) -> UserRead:
        result = await db.execute(select(User).where(User.username == user_in.username))
        if not (user := result.scalar()) or not (verify_hash(user_in.password, str(user.password_hash or ''))):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User or password incorrect")
        return await generate_jwt_for_user(user, request, db)


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, request: Request, db: AsyncSession = Depends(get_db)) -> UserRead:
    result = await db.execute(select(User).where(User.username == user_in.username))
    if result.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = User(
        username=user_in.username,
        email=user_in.email,
        password_hash=create_hash(user_in.password)
    )
    return await generate_jwt_for_user(user, request, db)
