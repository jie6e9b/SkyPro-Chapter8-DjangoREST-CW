"""Модели для интеграции с Telegram."""
from django.conf import settings
from django.db import models

class TelegramProfile(models.Model):
    """Профиль с привязкой chat_id к пользователю."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_id = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.user.username} -> {self.chat_id}"
