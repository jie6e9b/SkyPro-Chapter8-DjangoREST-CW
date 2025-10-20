"""Задачи Celery для домена привычек."""

from celery import shared_task
from django.contrib.auth import get_user_model

from .models import Habit
from telegram_app.client import send_message

User = get_user_model()


@shared_task
def send_habit_reminder(habit_id: int):
    """Отправляет пользователю напоминание о привычке в Telegram.

    Аргументы:
        habit_id: идентификатор привычки.
    """
    try:
        habit = Habit.objects.select_related("user").get(id=habit_id)
    except Habit.DoesNotExist:
        return

    user = habit.user
    # Ищем связанный профиль Telegram
    try:
        profile = user.telegramprofile
    except Exception:
        profile = None

    if not profile or not profile.chat_id:
        return

    text = (
        f"Напоминание о привычке:\n"
        f"Действие: {habit.action}\n"
        f"Место: {habit.place}\n"
        f"Время: {habit.time.strftime('%H:%M')}\n"
    )
    send_message(chat_id=profile.chat_id, text=text)
