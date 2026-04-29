from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Product, Category, Order, Profile
from app.schemas import (
    UserCreate, UserResponse, UserUpdate,
    ProductResponse, CategoryResponse, OrderResponse, ProfileResponse
)
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# --- ІСНУЮЧИЙ CRUD ДЛЯ USER (Лаба 3-4) ---

@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Цей email вже зареєстровано")

    new_user = User(
        email=user_data.email,
        hashed_password=user_data.password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.hashed_password = user_data.password
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    await db.delete(user)
    await db.commit()
    return {"message": f"Користувача з ID {user_id} видалено"}


# --- НОВІ РУЧКИ ДЛЯ ЛАБИ 4 (Додаткові моделі) ---

# Отримати профіль конкретного користувача (One-to-One)
@router.get("/{user_id}/profile", response_model=ProfileResponse, tags=["Lab 4 Extra"])
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Профіль не знайдено")
    return profile

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