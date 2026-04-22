import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Визначаємо шлях до .env, який лежить на рівень вище папки app
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # extra="ignore" дозволяє ігнорувати інші змінні в .env, якщо вони там є
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore")

settings = Settings()