# Habits API — трекер полезных привычек

Проект — бэкенд для SPA-приложения по книге «Атомные привычки». Сервис позволяет пользователям создавать и отслеживать полезные привычки, задавать периодичность и вознаграждения, публиковать свои привычки для примера другим, а также получать напоминания в Telegram через Celery.

## Возможности
- Регистрация и авторизация (JWT)
- CRUD для привычек текущего пользователя
- Публичный список привычек (только чтение)
- Пагинация списков (по 5 элементов на страницу по умолчанию)
- Валидация бизнес-правил (см. ниже)
- Интеграция с Telegram: привязка chat_id и отправка напоминаний задачами Celery
- CORS для фронтенда
- Документация OpenAPI и Swagger UI

## Бизнес-правила привычек
- Нельзя одновременно указывать вознаграждение и связанную приятную привычку
- В связанные привычки могут попадать только привычки с признаком «приятная»
- У приятной привычки не может быть вознаграждения или связанной привычки
- Время выполнения ≤ 120 секунд
- Периодичность: от 1 до 7 дней (не реже раза в 7 дней)

## Технологический стек
- Python 3.13, Django 5, Django REST Framework
- JWT (djangorestframework-simplejwt)
- Celery + Redis (broker/result backend)
- drf-spectacular (OpenAPI/Swagger)
- pytest (+ pytest-django, freezegun), flake8

## Быстрый старт
1) Клонируйте репозиторий

2) Создайте и заполните .env (см. .env.example)

3) Установите зависимости через Poetry:
  - poetry install

4) Примените миграции БД:
- python manage.py migrate

5) Запустите сервер разработки:
- python manage.py runserver

6) (Опционально) Запустите Celery для напоминаний:
- celery -A config worker -l info

7) (Опционально) Запустите Redis (если не поднят):
- локально: redis-server
- либо используйте любой доступный Redis по адресу из переменных окружения

## Переменные окружения (.env)
См. .env.example. Ключевые:
- SECRET_KEY — секретный ключ Django 
- DEBUG — true/false
- ALLOWED_HOSTS — список хостов через запятую
- CORS_ALLOWED_ORIGINS — список источников фронтенда через запятую
- POSTGRES_DB/USER/PASSWORD/HOST/PORT — параметры БД (в тестах автоматически используется SQLite)
- CELERY_BROKER_URL / CELERY_RESULT_BACKEND — адреса Redis для Celery
- TELEGRAM_BOT_TOKEN — токен Telegram-бота для отправки сообщений
- TIME_ZONE — часовой пояс (например, Europe/Moscow)

Примечание: В тестах БД переключается на SQLite in-memory, чтобы не требовать внешний Postgres.

## API и эндпоинты
Базовый префикс: /api/

Аутентификация
- POST /api/accounts/register/ — регистрация пользователя
- POST /api/accounts/token/obtain/ — выдача JWT access/refresh
- POST /api/accounts/token/refresh/ — обновление access по refresh

Привычки (требуется аутентификация)
- GET /api/habits/ — список привычек текущего пользователя (пагинация по 5)
- POST /api/habits/ — создать привычку
- GET /api/habits/{id}/ — получить
- PUT/PATCH /api/habits/{id}/ — обновить
- DELETE /api/habits/{id}/ — удалить

Публичные привычки (без авторизации)
- GET /api/habits/public/ — список только публичных привычек

Telegram
- POST /api/telegram/link/ — привязать chat_id к текущему пользователю
  - body: {"chat_id": "<строка>"}
- DELETE /api/telegram/unlink/ — отвязать chat_id

Документация
- OpenAPI: GET /api/schema/
- Swagger UI: GET /api/docs/

## Модель Habit
Поля (основные):
- user — владелец (создатель)
- place — место выполнения
- time — время выполнения
- action — действие
- is_pleasant — признак приятной привычки
- related_habit — ссылка на приятную привычку (для полезной привычки)
- periodicity — периодичность (1…7 дней), по умолчанию 1
- reward — вознаграждение (строка)
- duration_seconds — длительность в секундах (≤ 120)
- is_public — признак публичности

## Права доступа
- Доступ к CRUD по привычкам — только у их владельца
- Публичный список доступен всем только на чтение

## Пагинация
- По умолчанию 5 элементов на страницу
- Параметры query: page=<num>

## Интеграция с Telegram
1) Создайте бота через @BotFather и получите токен
2) Запишите токен в TELEGRAM_BOT_TOKEN в .env
3) Получите chat_id пользователя (можно отправить сообщение вашему боту, затем найти chat_id через Telegram API либо через временную ручку/логирование)
4) Привяжите chat_id к профилю: POST /api/telegram/link/ {"chat_id":"..."}
5) Запустите Celery worker для отправки напоминаний

Отправка сообщений реализована в telegram_app.client.send_message(). Для продакшена рекомендуется добавить логирование и обработку ошибок.

## Тесты и линтер
- Запуск тестов: pytest -q
- Покрытие выводится в консоль (цель ≥ 80%)
- Запуск flake8: flake8

## Разработка
- Конфигурация DRF (аутентификация, пагинация) — в config/settings.py
- Бизнес-валидаторы — habits/validators.py
- Задачи Celery — habits/tasks.py
- Документация OpenAPI — drf-spectacular (config/urls.py)

## Лицензия
MIT 
