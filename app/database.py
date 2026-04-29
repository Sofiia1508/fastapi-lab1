from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Створюємо асинхронний двигун (engine)
# Використовуємо DATABASE_URL, який ми прописали в config.py
engine = create_async_engine(settings.DATABASE_URL)

# Створюємо фабрику сесій.
# expire_on_commit=False потрібно для асинхронної роботи, щоб об'єкти не "пропадали" після коміту
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

# Базовий клас для всіх майбутніх моделей (таблиць)
class Base(DeclarativeBase):
    pass

# Функція-залежність (Dependency) для FastAPI.
# Вона буде відкривати сесію для кожного запиту і автоматично закривати її
async def get_db():
    async with async_session_factory() as session:
        yield session