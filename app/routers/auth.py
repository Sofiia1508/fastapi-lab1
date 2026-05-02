from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timedelta

# Імпортуємо налаштування та базу
from app.database import get_db
from app import models  # Імпортуємо весь модуль моделей
from app.schemas import UserCreate, UserLogin, UserResponse
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# 1. РЕЄСТРАЦІЯ
@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Користувач з таким email вже існує"
        )

    hashed = hash_password(user_data.password)

    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# 2. АУТЕНТИФІКАЦІЯ (Login)
@router.post("/login")
async def login(
        response: Response,
        user_data: UserLogin,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(models.User).filter(models.User.email == user_data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email або пароль"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )

    return {"message": "Вхід виконано успішно"}

# 3. ВИХІД (Logout)
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вихід виконано"}

# --- ЗАХИЩЕНІ РУЧКИ ---

# 4. ОТРИМАТИ СВІЙ ПРОФІЛЬ
@router.get("/me")
async def get_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "status": "success"
    }

# 5. ПЕРЕВІРКА АВТОРИЗАЦІЇ
@router.get("/check-status")
async def check_status(current_user: models.User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "message": "Ви успішно пройшли перевірку через JWT у Cookies!"
    }