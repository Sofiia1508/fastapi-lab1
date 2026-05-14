import pytest
import time
from httpx import AsyncClient


# --- ГРУПА ТЕСТІВ: AUTH (Авторизація та реєстрація) ---

@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient):
    """Перевірка ручки POST /auth/register"""
    unique_email = f"user_{int(time.time())}@example.com"
    response = await ac.post("/auth/register", json={
        "email": unique_email,
        "password": "strong_password123"
    })
    assert response.status_code in [200, 201]
    assert response.json()["email"] == unique_email


@pytest.mark.asyncio
async def test_login_user(ac: AsyncClient):
    """Перевірка ручки POST /auth/login"""
    email = f"login_{int(time.time())}@example.com"
    password = "testpassword"

    # Створюємо користувача для входу
    await ac.post("/auth/register", json={"email": email, "password": password})

    # Спроба входу
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Вхід виконано успішно"


# --- ГРУПА ТЕСТІВ: PRODUCT (Робота з БД товарів, категорій та замовлень) ---

@pytest.mark.asyncio
async def test_get_all_products(ac: AsyncClient):
    """Перевірка ручки GET /product/all/products (Функція БД: select(Product))"""
    response = await ac.get("/product/all/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_all_categories(ac: AsyncClient):
    """Перевірка ручки GET /product/all/categories (Функція БД: select(Category))"""
    response = await ac.get("/product/all/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_user_orders(ac: AsyncClient):
    """Перевірка ручки GET /product/{user_id}/orders (Функція БД: select(Order))"""
    # Тестуємо на існуючому або неіснуючому ID
    user_id = 1
    response = await ac.get(f"/product/{user_id}/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# --- ГРУПА ТЕСТІВ: SYSTEM (Загальні перевірки) ---

@pytest.mark.asyncio
async def test_root_endpoint(ac: AsyncClient):
    """Перевірка головної ручки GET /"""
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "WORKS 100%"}