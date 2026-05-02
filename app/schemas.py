from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Користувач ---

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# ОСЬ ТУТ ВИПРАВЛЕНО:
class UserResponse(UserBase):
    id: int
    is_active: bool  # Розкоментуй і зроби обов'язковим, бо в базі воно True/False

    class Config:
        from_attributes = True


# --- Решта твоїх схем (залишаємо без змін, вони ок) ---

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
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