from __future__ import annotations
import os
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from app.routers import users, product, auth
from app.database import engine, Base
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

# 1. Змінюємо назву метрики на абсолютно нову для тесту
MY_CUSTOM_GAUGE = Gauge(
    "final_test_price",
    "Сумарна вартість товарів для фінальної перевірки"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Дія при старті: перевіряємо таблиці в БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Встановлюємо значення для НОВОЇ метрики
    MY_CUSTOM_GAUGE.set(1250.50)
    print(">>> Метрику final_test_price встановлено на 1250.50 <<<")

    yield
    await engine.dispose()


app = FastAPI(
    title="User Management API",
    description="Лабораторна робота №7: Моніторинг",
    version="1.0.0",
    lifespan=lifespan
)

# 2. Твої роутери (залишаємо на місці)
app.include_router(users.router)
app.include_router(product.router)
app.include_router(auth.router)


# 3. НОВИЙ ЕНДПОІНТ, щоб уникнути конфліктів за шлях /metrics
@app.get("/my-metrics")
def get_metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/")
def root():
    return {"status": "WORKS 100%"}