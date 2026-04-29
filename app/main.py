from fastapi import FastAPI
from app.routers import users
from app.database import engine, Base
# ВАЖЛИВО: Імпортуй моделі, щоб Base "побачив" таблицю users
from app import models

# 1. Спочатку створюємо об'єкт app
app = FastAPI(
    title="User Management API",
    description="Лабораторна робота №3: CRUD для користувачів з валідацією Pydantic",
    version="1.0.0"
)

# 2. Визначаємо функцію ініціалізації
async def init_db():
    async with engine.begin() as conn:
        # Це створить таблиці у Postgres, якщо їх ще немає
        await conn.run_sync(Base.metadata.create_all)

# 3. Підключаємо подію старту (тепер об'єкт app вже існує)
@app.on_event("startup")
async def on_startup():
    await init_db()

# 4. Підключаємо роутери
app.include_router(users.router)

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "API працює. Перейдіть до /docs"
    }