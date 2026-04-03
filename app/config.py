from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ці назви мають ТОЧНО збігатися з назвами у файлі .env
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        # Формуємо рядок для асинхронного підключення через драйвер asyncpg
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Вказуємо Pydantic шукати файл .env на рівень вище від папки app
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Створюємо екземпляр, який будемо імпортувати в інші файли
settings = Settings()