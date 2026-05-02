from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

# Базовий клас
class Base(DeclarativeBase):
    pass




async def get_db():
    async with async_session_factory() as session:
        yield session