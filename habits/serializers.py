"""Сериализаторы для модели Habit."""

from rest_framework import serializers

from .models import Habit
from .validators import validate_habit_business_rules


class HabitSerializer(serializers.ModelSerializer):
    """Базовый сериализатор Habit с бизнес-валидацией."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "duration_seconds",
            "is_public",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        """Вызывает проверку бизнес-правил перед сохранением."""
        instance = getattr(self, "instance", None)
        return validate_habit_business_rules(attrs, instance)
