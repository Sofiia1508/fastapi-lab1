from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserUpdate
from typing import List

# Створюємо роутер
router = APIRouter(prefix="/users", tags=["Users"])


# 1. СТВОРЕННЯ (POST) - Тепер записує в Postgres
@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Перевіряємо, чи такий email вже існує в базі
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Цей email вже зареєстровано")

    # Створюємо новий об'єкт моделі
    new_user = User(
        email=user_data.email,
        hashed_password=user_data.password  # У лабі 4 поки зберігаємо просто пароль
    )

    db.add(new_user)
    await db.commit()  # Зберігаємо в базу
    await db.refresh(new_user)  # Отримуємо згенерований базою ID
    return new_user


# 2. ОТРИМАННЯ ВСІХ (GET)
@router.get("/", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()


# 3. ОТРИМАННЯ ОДНОГО ЗА ID (GET)
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return user


# 4. ОНОВЛЕННЯ (PUT/PATCH)
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    # Оновлюємо поля
    if user_data.email:
        user.email = user_data.email
    if user_data.password:
        user.hashed_password = user_data.password

    await db.commit()
    await db.refresh(user)
    return user


# 5. ВИДАЛЕННЯ (DELETE)
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    await db.delete(user)
    await db.commit()
    return {"message": f"Користувача з ID {user_id} видалено з бази даних"}