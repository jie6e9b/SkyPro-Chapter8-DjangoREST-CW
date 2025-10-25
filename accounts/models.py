"""Модель пользователя для проекта. Определяет кастомную модель User, использующую email вместо username для авторизации."""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Кастомная модель пользователя, наследуемая от AbstractUser.
    Использует email как уникальный идентификатор вместо username.
    """
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """Возвращает строковое представление пользователя — его email."""
        return self.email