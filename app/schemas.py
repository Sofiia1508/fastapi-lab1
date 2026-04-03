from pydantic import BaseModel, EmailStr
from typing import Optional

# Базова схема
class UserBase(BaseModel):
    email: EmailStr

# Схема для створення (те, що ми шлемо в POST)
class UserCreate(UserBase):
    password: str

# Схема для оновлення (PUT)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Схема для відповіді сервера (те, що бачимо в Postman)
class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True