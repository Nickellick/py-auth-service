from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy.future import select
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    async def register(user_in: UserCreate, db: AsyncSession):
        result = await db.execute(select(User).where(User.username == user_in.username))
        if result.scalar():
            raise HTTPException(status_code=400, detail="Username already exists")
        user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=get_password_hash(user_in.password)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def login(user_in: UserLogin, db: AsyncSession):
        result = await db.execute(select(User).where(User.username == user_in.username))
        if not (user := result.scalar()):
            raise HTTPException(status_code=404, detail="User not found")
        return user
    # TODO create token and return it