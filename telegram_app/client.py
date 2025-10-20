"""Клиент для обращения к Telegram Bot API.
Минимальная обёртка для отправки текстовых сообщений."""

import os
import requests
from django.conf import settings


def get_bot_token() -> str:
    """Возвращает токен бота из настроек/окружения."""
    return getattr(settings, "TELEGRAM_BOT_TOKEN", None) or os.getenv("TELEGRAM_BOT_TOKEN", "")


def send_message(chat_id: str, text: str) -> None:
    """Отправляет текстовое сообщение в чат Telegram.
    Если токен не задан — функция завершится без ошибки."""
    token = get_bot_token()
    if not token:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        # Логирование можно добавить позже
        pass
