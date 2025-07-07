from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import DB_CONFIG

engine = create_async_engine(DB_CONFIG["url"], echo=DB_CONFIG["echo"])
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session