import datetime

from fastapi import Request, Depends
from jwt import encode, decode
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_hash
from app.dependencies.db import get_db
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.user import UserRead
from config import config

async def generate_jwt_for_user(user: User, request: Request, db: AsyncSession = Depends(get_db)) -> UserRead:
    user_agent = request.headers.get("user-agent", "unknown")
    ip = request.client.host if request.client and request.client.host else "unknown"
    issued_at = datetime.datetime.now(datetime.UTC)
    refresh_expires_at = issued_at + datetime.timedelta(days=config.jwt.refresh_token_expire_days)
    access_expired_at = issued_at + datetime.timedelta(minutes=config.jwt.access_token_expire_minutes)
    refresh_token = encode({
        'refresh': True,
        'uid': user.id,
        'iat': issued_at.isoformat(),
        'exp': refresh_expires_at.isoformat(),
        'roles': user.roles,
    }, algorithm=config.jwt.algorithm, key=config.jwt.key)
    access_token = encode({
        'refresh': False,
        'uid': user.id,
        'iat': issued_at.isoformat(),
        'exp': access_expired_at.isoformat(),
        'roles': user.roles,
    }, algorithm=config.jwt.algorithm, key=config.jwt.key)
    db_token = RefreshToken(
        user_id=user.id,
        issued_at=issued_at,
        expires_at=refresh_expires_at,
        refresh_token_hash=create_hash(refresh_token),
        user_agent=user_agent,
        ip_address=ip
    )
    db.add(db_token)
    user.refresh_tokens.append(db_token)
    await db.commit()
    await db.refresh(user)
    response = UserRead.model_validate(user)
    response.access_token = access_token
    response.refresh_token = refresh_token
    return response


async def verify_jwt(user: User, token: str, request: Request, db: AsyncSession = Depends) -> UserRead:
    token_data = decode(token, algorithm=config.jwt.algorithm, key=config.jwt.key, verify=True)
    if not token_data.get('refresh', False):
        raise Exception("Invalid token data")
    if not (user_token := await db.get(RefreshToken, token_data['uid'])):
        raise Exception("Invalid token data")
    if user_token.is_revoked:
        raise Exception("Refresh token is revoked")
    if user_token.expires_at < datetime.datetime.now(datetime.UTC):
        user_token.revoked_at = datetime.datetime.now(datetime.UTC)
        user_token.is_revoked = True
        await db.commit()
    return await generate_jwt_for_user(user, request, db)