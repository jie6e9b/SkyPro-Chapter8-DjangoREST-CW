# 🎯 Habits API - Трекер полезных привычек

Backend API для приложения трекера привычек на основе Django REST Framework.

## 📋 Содержание

- [Возможности](#возможности)
- [Технологический стек](#технологический-стек)
- [Структура проекта](#структура-проекта)
- [Быстрый старт](#быстрый-старт)
- [CI/CD](#cicd)
- [API документация](#api-документация)
- [Тестирование](#тестирование)

---

## 🚀 Возможности

- ✅ CRUD операции с привычками
- ✅ Публичные и приватные привычки с пагинацией
- ✅ JWT аутентификация (email вместо username)
- ✅ Celery для фоновых задач
- ✅ Telegram уведомления о привычках
- ✅ Валидация бизнес-правил
- ✅ Docker контейнеризация
- ✅ Автоматические CI/CD через GitHub Actions

### Бизнес-правила привычек
- Нельзя одновременно указывать вознаграждение и связанную приятную привычку
- В связанные привычки могут попадать только привычки с признаком «приятная»
- У приятной привычки не может быть вознаграждения или связанной привычки
- Время выполнения ≤ 120 секунд
- Периодичность: от 1 до 7 дней

---

## 🛠 Технологический стек

- **Backend:** Django 5.2, Django REST Framework 3.16
- **Database:** PostgreSQL 16
- **Cache/Broker:** Redis 7
- **Task Queue:** Celery 5.5
- **WSGI Server:** Gunicorn 21.2 (prod)
- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Testing:** pytest, pytest-django (покрытие 86%)
- **Code Quality:** flake8
- **Documentation:** drf-spectacular (OpenAPI 3.0)

---

## 📁 Структура проекта

```
📁 SkyPro-Chapter8-DjangoREST-CW/
│
├── 📁 .github/workflows/        # GitHub Actions CI/CD
│   └── ci-cd.yml               # Pipeline: lint → test → build → deploy
│
├── 📁 accounts/                # Аутентификация пользователей (JWT с email)
├── 📁 habits/                  # CRUD привычек с пагинацией
├── 📁 telegram_app/            # Telegram интеграция
├── 📁 config/                  # Django settings
├── 📁 tests/                   # Тесты (17 тестов, 86% покрытие)
│
├── Dockerfile                  # Универсальный (dev + prod через ARG)
├── docker-compose.yml          # Для разработки
├── docker-compose.prod.yml     # Для продакшена
├── nginx.conf                  # Nginx конфигурация
│
├── requirements.txt            # Базовые зависимости + gunicorn
├── requirements-dev.txt        # Dev зависимости (pytest, flake8)
│
├── .env                        # Переменные окружения (dev)
├── .env.prod.example           # Шаблон для продакшена
│
├── CICD_SETUP.md              # Полная инструкция по настройке CI/CD
├── DEPLOYMENT_CHEATSHEET.md   # Шпаргалка команд для деплоя
└── README.md                   # Этот файл
```

---

## 🏃 Быстрый старт

### Локальная разработка с Docker (рекомендуется)

1. **Клонировать репозиторий:**
```bash
git clone https://github.com/your-username/habits-api.git
cd habits-api
```

2. **Создать `.env` файл:**
```bash
cp .env.example .env
# Отредактируйте .env своими значениями
```

3. **Запустить приложение:**
```bash
docker-compose up --build
```

4. **Приложение доступно:**
- API: http://localhost:8000/api/
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/
- Admin: http://localhost:8000/admin/

5. **Создать суперпользователя:**
```bash
docker-compose exec web python manage.py createsuperuser
```

### Без Docker (локальная разработка)

```bash
# 1. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# 2. Установить зависимости
pip install -r requirements-dev.txt

# 3. Настроить БД и запустить
python manage.py migrate
python manage.py runserver

# 4. (Опционально) Запустить Celery
celery -A config worker -l info
```

---

## 🔄 CI/CD

### Автоматический деплой

При пуше в ветку `feature-1` запускается полный pipeline:

```
Push → Lint → Test → Build → Push to Docker Hub → Deploy → Notify
  ↓      ↓      ↓       ↓            ↓               ↓        ↓
 Git   flake8  pytest  Docker    DockerHub    SSH+Server   Status
```

**Этапы:**
1. **Lint** - flake8 проверка качества кода
2. **Test** - pytest с PostgreSQL/Redis (17 тестов, 86% покрытие)
3. **Build** - Сборка Docker образа с `ENV=prod`
4. **Push** - Загрузка в Docker Hub
5. **Deploy** - SSH деплой на сервер через docker-compose
6. **Notify** - Уведомление о статусе деплоя

**Подробная инструкция:** См. [CICD_SETUP.md](CICD_SETUP.md)

---

## 📚 API Документация

### Основные эндпоинты:

#### Аутентификация (JWT с email)
```bash
POST /api/accounts/register/          # Регистрация (email + password)
POST /api/accounts/token/obtain/      # Получить JWT токен (email + password)
POST /api/accounts/token/refresh/     # Обновить access token
```

#### Привычки (требуется JWT токен)
```bash
GET    /api/habits/                   # Список своих привычек (пагинация 5 шт)
POST   /api/habits/                   # Создать привычку
GET    /api/habits/{id}/              # Детали привычки
PUT    /api/habits/{id}/              # Обновить привычку
PATCH  /api/habits/{id}/              # Частично обновить
DELETE /api/habits/{id}/              # Удалить привычку

GET    /api/habits/public/            # Публичные привычки (пагинация)
```

#### Telegram
```bash
POST   /api/telegram/link/            # Привязать Telegram чат ID
POST   /api/telegram/unlink/          # Отвязать Telegram
```

### Интерактивная документация

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/

### Пример запроса (регистрация):

```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Str0ngP@ssw0rd"
  }'
```

---

## 🧪 Тестирование

### Запуск тестов в Docker

```bash
# Все тесты
docker-compose exec web python -m pytest -v

# С покрытием кода
docker-compose exec web python -m pytest --cov=. --cov-report=term-missing

# HTML отчет покрытия
docker-compose exec web python -m pytest --cov=. --cov-report=html
open htmlcov/index.html

# Конкретный файл
docker-compose exec web python -m pytest tests/test_habits.py -v

# Один тест
docker-compose exec web python -m pytest tests/test_habits.py::test_create_and_list_own_habits -v
```

### Статистика тестов
- ✅ **17 тестов** - все проходят
- ✅ **86% покрытие кода** (506 строк)
- ✅ Тестируются: habits, accounts, permissions, validators, telegram

### Запуск линтера

```bash
# Flake8
docker-compose exec web flake8 .

# Строгая проверка
docker-compose exec web flake8 . --count --select=E9,F63,F7,F82 --show-source
```

---

## 🐳 Docker команды

### Разработка (docker-compose.yml)

```bash
# Запустить все сервисы
docker-compose up

# Пересобрать и запустить
docker-compose up --build

# В фоновом режиме
docker-compose up -d

# Остановить
docker-compose down

# Логи
docker-compose logs -f web
docker-compose logs -f celery

# Django команды
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell

# Зайти в контейнер
docker-compose exec web bash

# Статус контейнеров
docker-compose ps
```

### Продакшен (docker-compose.prod.yml)

```bash
# Запустить prod окружение
docker-compose -f docker-compose.prod.yml up -d

# Обновить образы из Docker Hub
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d

# Применить миграции
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

**Полная шпаргалка:** См. [DEPLOYMENT_CHEATSHEET.md](DEPLOYMENT_CHEATSHEET.md)

---

## 🔧 Конфигурация

### Переменные окружения (.env)

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=habits_db
POSTGRES_USER=habits_user
POSTGRES_PASSWORD=your-strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis/Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# JWT
ACCESS_TOKEN_MINUTES=60
REFRESH_TOKEN_DAYS=7

# Pagination
PAGE_SIZE=5

# Telegram
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### Dockerfile - Универсальный

Один Dockerfile для dev и prod через аргумент `ENV`:

```bash
# Сборка для разработки (с pytest, flake8)
docker build --build-arg ENV=dev -t habits-api:dev .

# Сборка для продакшена (только базовые зависимости + gunicorn)
docker build --build-arg ENV=prod -t habits-api:prod .
# или просто (prod по умолчанию)
docker build -t habits-api:prod .
```

**Преимущества:**
- ✅ Один файл вместо двух
- ✅ Условная установка зависимостей
- ✅ Проще поддерживать и обновлять

---

## 🚢 Деплой

### Ручной деплой

```bash
# 1. Собрать и загрузить образ
docker build --build-arg ENV=prod -t your-username/habits-api:latest .
docker push your-username/habits-api:latest

# 2. На сервере
cd /path/to/project
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

### Автоматический деплой через GitHub Actions

Просто запушьте изменения в ветку `feature-1`:

```bash
git add .
git commit -m "Your changes"
git push origin feature-1
```

GitHub Actions автоматически:
- ✅ Запустит линтеры
- ✅ Запустит тесты
- ✅ Соберет Docker образ
- ✅ Загрузит в Docker Hub
- ✅ Задеплоит на сервер
- ✅ Применит миграции

**Статус деплоя:** GitHub → Actions → CI/CD Pipeline

---

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📝 Полезные ссылки

- **CI/CD настройка:** [CICD_SETUP.md](CICD_SETUP.md) - Пошаговая инструкция
- **Команды деплоя:** [DEPLOYMENT_CHEATSHEET.md](DEPLOYMENT_CHEATSHEET.md) - Шпаргалка
- **Swagger UI:** `/api/docs/` - Интерактивная документация API
- **ReDoc:** `/api/redoc/` - Альтернативная документация

---

## 📄 Лицензия

MIT License

---

## 🎓 Проект создан в рамках курса SkyPro

**Chapter 8:** Django REST Framework - Курсовая работа

---

**Готово к использованию!** 🚀

Для начала работы следуйте разделу [Быстрый старт](#быстрый-старт).
