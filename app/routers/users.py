from fastapi import APIRouter, HTTPException
from app.schemas import UserCreate, UserResponse, UserUpdate
from typing import List

# Створюємо роутер.
# prefix="/users" означає, що всі запити будуть починатися з http://localhost:8000/users
router = APIRouter(prefix="/users", tags=["Users"])

# ⚠️ Емуляція бази даних (звичайний словник)
db_users = {}
id_counter = 1


# 1. СТВОРЕННЯ (POST)
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global id_counter
    # Перетворюємо дані з Postman у словник і додаємо ID
    new_user = {"id": id_counter, **user.model_dump()}
    db_users[id_counter] = new_user
    id_counter += 1
    return new_user


# 2. ОТРРИМАННЯ ВСІХ (GET)
@router.get("/", response_model=List[UserResponse])
def get_all_users():
    return list(db_users.values())


# 3. ОТРРИМАННЯ ОДНОГО ЗА ID (GET)
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return db_users[user_id]


# 4. ОНОВЛЕННЯ (PUT)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    stored_user = db_users[user_id]
    # Оновлюємо тільки ті поля, які прийшли в запиті
    update_dict = user_data.model_dump(exclude_unset=True)
    updated_user = {**stored_user, **update_dict}

    db_users[user_id] = updated_user
    return updated_user


# 5. ВИДАЛЕННЯ (DELETE)
@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in db_users:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    del db_users[user_id]
    return {"message": f"Користувача з ID {user_id} видалено успішно"}