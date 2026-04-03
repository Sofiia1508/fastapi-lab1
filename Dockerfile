FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Встановлюємо залежності для бази даних (необхідні для asyncpg/psycopg)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Встановлюємо poetry
RUN pip install --no-cache-dir poetry

# Копіюємо ТІЛЬКИ файл конфігурації (без lock-файлу, щоб уникнути конфліктів)
COPY pyproject.toml /app/

# Налаштовуємо poetry: не створювати віртуальне середовище всередині контейнера
# та генеруємо новий lock-файл прямо під час збірки
RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --no-root --no-interaction --no-ansi

# Копіюємо решту коду
COPY . /app

# Команда для запуску
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]