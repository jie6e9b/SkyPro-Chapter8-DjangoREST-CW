# Базовый образ
FROM python:3.13-slim
LABEL authors="jie6e9b"

# Настройки окружения
ENV PYTHONUNBUFFERED=1

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя
RUN useradd --create-home --shell /bin/bash app

# Рабочая директория
WORKDIR /app

# Копирование и установка зависимостей
COPY requirements.txt requirements-dev.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

# Копирование проекта с назначением владельца
COPY --chown=app:app . .

USER app

# Команда по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]