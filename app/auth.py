from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from sqlalchemy.orm import selectinload

# Налаштування безпеки
SECRET_KEY = "sofia_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    from app.models import User
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload # Імпортуємо для безпечного завантаження
    from jose import JWTError

    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не знайдено в куках"
        )

    token = token.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Невалідний токен: відсутній email")
    except JWTError:
        raise HTTPException(status_code=401, detail="Помилка декодування токена")

    try:
        # ВИПРАВЛЕНО: Додаємо selectinload(User.profile) про всяк випадок,
        # щоб SQLAlchemy не падала при спробі доступу до зв'язків
        query = select(User).where(User.email == email).options(selectinload(User.profile))
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=401, detail="Користувача не знайдено")

        return user

    except Exception as e:
        # Тепер ми точно побачимо, що болить: база, модель чи сесія
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Помилка при роботі з базою",
                "error_type": type(e).__name__,
                "error_details": str(e)
            }
        )