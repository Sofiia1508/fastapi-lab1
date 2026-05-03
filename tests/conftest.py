import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import Base, get_db

# Дані з твого .env (перевірено за скріншотами)
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/beauty_shop_test"

# NullPool гарантує, що кожна операція отримає чисте з'єднання
test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
test_async_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    # Створюємо таблиці один раз на всю сесію тестів
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def override_get_db():
    async with test_async_session_factory() as session:
        yield session

# Підміна залежності
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(scope="function")
async def ac():
    # Створюємо клієнт окремо для кожного тесту
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client