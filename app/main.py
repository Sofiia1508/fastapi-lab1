from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import func, select

from app.database import Base, async_session_factory, engine
from app.models import Order, Product
from app.routers import auth, product, users

ORDERS_TOTAL_AMOUNT = Gauge(
    "app_orders_total_amount_uah",
    "Sum of Order.total_amount for all orders in the database",
)
INVENTORY_LIST_VALUE = Gauge(
    "app_inventory_list_price_total",
    "Sum of Product.price * Product.stock across all products",
)


async def refresh_business_metrics() -> None:
    async with async_session_factory() as session:
        total_orders = await session.scalar(
            select(func.coalesce(func.sum(Order.total_amount), 0.0))
        )
        ORDERS_TOTAL_AMOUNT.set(float(total_orders or 0))
        inventory_val = await session.scalar(
            select(func.coalesce(func.sum(Product.price * Product.stock), 0.0))
        )
        INVENTORY_LIST_VALUE.set(float(inventory_val or 0))


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await refresh_business_metrics()

    async def metrics_loop() -> None:
        while True:
            await asyncio.sleep(30)
            await refresh_business_metrics()

    task = asyncio.create_task(metrics_loop())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    await engine.dispose()


app = FastAPI(
    title="User Management API",
    description="Лабораторна робота №7: Моніторинг",
    version="1.0.0",
    lifespan=lifespan,
)

Instrumentator(
    should_group_status_codes=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/my-metrics"],
).instrument(app).expose(app, endpoint="/my-metrics", include_in_schema=False)

app.include_router(users.router)
app.include_router(product.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"status": "WORKS 100%"}
