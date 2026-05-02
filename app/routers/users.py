from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Request  # Додай Request сюди
from jose import JWTError, jwt  # Для роботи з токеном
from app.auth import SECRET_KEY, ALGORITHM  # Імпортуємо константи з нашого файлу auth
from app.models import User, Product, Category, Order, Profile
from app.schemas import (
    UserCreate, UserResponse, UserUpdate,
    ProductResponse, CategoryResponse, OrderResponse, ProfileResponse
)
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# --- ІСНУЮЧИЙ CRUD ДЛЯ USER (Лаба 3-4) ---

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Не авторизований (відсутні кукі)")

    token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Недійсний токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Помилка токена")

    # ОСЬ ТУТ БУЛА ПОМИЛКА (Рядок 59):
    # Замість db.query(User)... пишемо асинхронний select
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")

    return user

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

