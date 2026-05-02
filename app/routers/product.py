from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Product, Category, Order
from app.schemas import (
    ProductResponse, CategoryResponse, OrderResponse)
from typing import List

router = APIRouter(prefix="/product", tags=["Product"])

# Отримати всі товари (Product)
@router.get("/all/products", response_model=List[ProductResponse], tags=["Lab 4 Extra"])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()

# Отримати всі категорії (Category)
@router.get("/all/categories", response_model=List[CategoryResponse], tags=["Lab 4 Extra"])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()

# Отримати замовлення користувача (Order)
@router.get("/{user_id}/orders", response_model=List[OrderResponse], tags=["Lab 4 Extra"])
async def get_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.user_id == user_id))
    return result.scalars().all()