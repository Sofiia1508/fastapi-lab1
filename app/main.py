from fastapi import FastAPI
from app.routers import users

# Створюємо головний об'єкт додатка
app = FastAPI(
    title="User Management API",
    description="Лабораторна робота №3: CRUD для користувачів з валідацією Pydantic",
    version="1.0.0"
)

# Підключаємо роутер користувачів.
# Тепер всі ендпоїнти з app/routers/users.py стануть частиною додатка.
app.include_router(users.router)

# Базовий маршрут для перевірки працездатності
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "API працює. Перейдіть до /docs для перегляду документації або використовуйте Postman."
    }