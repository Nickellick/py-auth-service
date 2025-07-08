from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import config

db = config.database

engine = create_async_engine(db.build_url(), echo=db.echo_db)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
