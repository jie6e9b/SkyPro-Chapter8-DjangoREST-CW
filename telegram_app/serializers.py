"""Сериализаторы для Telegram-профилей."""
from rest_framework import serializers
from .models import TelegramProfile


class TelegramProfileSerializer(serializers.ModelSerializer):
    """Сериализатор привязки chat_id к пользователю."""
    class Meta:
        model = TelegramProfile
        fields = ("chat_id",)
