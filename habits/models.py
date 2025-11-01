"""Модели домена привычек.
Содержит модель Habit со всеми необходимыми полями и индексами """

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Habit(models.Model):
    """Привычка пользователя.
    - Полезная привычка: действие, которое пользователь совершает, и за которое
      получает вознаграждение (reward) или связанную «приятную» привычку.
    - Приятная привычка: отмечается флагом is_pleasant и не может иметь
      вознаграждения или связанных привычек.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    reward = models.CharField(max_length=255, blank=True, default="")
    duration_seconds = models.PositiveSmallIntegerField(
        default=60, validators=[MinValueValidator(1), MaxValueValidator(120)]
    )
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_public"]),
        ]

    def __str__(self):
        return f"{self.action} @ {self.time} in {self.place}"
