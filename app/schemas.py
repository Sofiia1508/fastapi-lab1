from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Користувач (Твій існуючий код) ---

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


# --- Нові схеми для Лаби №5 (Авторизація) ---

class UserLogin(BaseModel):
    """Схема для входу (те, що юзер шле при логіні)"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Схема для повернення токена (якщо знадобиться)"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Схема для даних, які ми 'зашиємо' всередину токена (email)"""
    email: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    full_name: str
    phone: Optional[str] = None
    user_id: int

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    title: str
    price: float
    category_id: int

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    status: str
    total_amount: float
    user_id: int

    class Config:
        from_attributes = True