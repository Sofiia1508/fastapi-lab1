from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import timedelta

# Імпортуємо твої налаштування
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# 1. РЕЄСТРАЦІЯ (Синхронна)
@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Перевіряємо, чи імейл вільний
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Користувач з таким email вже існує"
        )

    # Хешуємо пароль
    hashed = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2. АУТЕНТИФІКАЦІЯ (Login)
@router.post("/login")
def login(
        response: Response,
        user_data: UserLogin,
        db: Session = Depends(get_db)
):
    # Шукаємо юзера
    user = db.query(User).filter(User.email == user_data.email).first()

    # Перевіряємо пароль
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email або пароль"
        )

    # Генеруємо JWT токен
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Записуємо токен у КУКИ
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
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Вихід виконано"}