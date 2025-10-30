# Универсальный Dockerfile для dev и prod окружений
FROM python:3.13-slim
LABEL authors="jie6e9b"
LABEL description="Universal Docker image for Habits API (dev/prod)"

# Аргумент для выбора окружения (dev или prod)
ARG ENV=prod

# Настройки окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя
RUN useradd --create-home --shell /bin/bash app

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt requirements-dev.txt ./

# Условная установка зависимостей в зависимости от окружения
RUN pip install --upgrade pip && \
    if [ "$ENV" = "dev" ]; then \
        echo "Installing DEV dependencies..." && \
        pip install --no-cache-dir -r requirements-dev.txt; \
    else \
        echo "Installing PROD dependencies..." && \
        pip install --no-cache-dir -r requirements.txt; \
    fi

# Копирование проекта с назначением владельца
COPY --chown=app:app . .

# Создание директорий для статики и медиа (для продакшена)
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R app:app /app/staticfiles /app/media

USER app

# Команда по умолчанию (для разработки - runserver, для прода будет переопределена в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
