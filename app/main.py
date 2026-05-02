import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import users, product, auth
from app.database import engine, Base
from fastapi import Request
from fastapi.responses import JSONResponse



# Використовуємо lifespan замість застарілого on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Дія при старті: перевіряємо таблиці
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Дія при вимкненні: закриваємо engine
    await engine.dispose()

app = FastAPI(
    title="User Management API",
    description="Лабораторна робота №3-5",
    version="1.0.0",
    lifespan=lifespan # Підключаємо життєвий цикл
)

# Підключаємо роутери
app.include_router(users.router)
app.include_router(product.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Я ТЕБЕ БАЧУ"}
