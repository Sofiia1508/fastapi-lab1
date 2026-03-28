from pydantic import BaseModel, EmailStr
from typing import Optional

# Базова схема з загальними полями для всіх операцій
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

# Схема для створення користувача (тут потрібен пароль)
# Використовується в POST запитах
class UserCreate(UserBase):
    password: str

# Схема для оновлення користувача (всі поля необов'язкові)
# Використовується в PUT запитах
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

# Схема для відповіді сервера (те, що бачить клієнт у Postman)
# Тут НЕМАЄ пароля з міркувань безпеки
class UserResponse(UserBase):
    id: int

    class Config:
        # Це дозволяє Pydantic працювати з об'єктами (якщо ми потім підключимо БД)
        from_attributes = True