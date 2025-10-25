"""Бизнес-валидаторы для домена привычек."""

from rest_framework import serializers

from .models import Habit


def validate_habit_business_rules(attrs, instance: Habit | None = None):
    """Проверяет бизнес-ограничения модели Habit.

    Аргументы:
        attrs: входящие данные сериализатора.
        instance: существующий объект Habit при обновлении (или None при создании).

    Поднимает serializers.ValidationError при нарушениях правил.
    """
    is_pleasant = attrs.get("is_pleasant", getattr(instance, "is_pleasant", False))
    reward = attrs.get("reward", getattr(instance, "reward", "")) or ""
    related_habit = attrs.get("related_habit", getattr(instance, "related_habit", None))
    duration_seconds = attrs.get(
        "duration_seconds", getattr(instance, "duration_seconds", 60)
    )
    periodicity = attrs.get("periodicity", getattr(instance, "periodicity", 1))

    # Время выполнения не больше 120 сек — покрыто валидатором поля, но проверим на всякий случай
    if duration_seconds > 120:
        raise serializers.ValidationError({"duration_seconds": "Не больше 120 секунд."})

    # # Нельзя реже, чем 1 раз в 7 дней — покрыто валидатором MaxValueValidator(7)
    # if not (1 <= periodicity <= 7):
    #     raise serializers.ValidationError({"periodicity": "Значение от 1 до 7 дней."})

    # Исключить одновременный выбор связанной привычки и вознаграждения
    if related_habit and reward:
        raise serializers.ValidationError(
            {
                "non_field_errors": [
                    "Нельзя одновременно указывать связанную приятную привычку и вознаграждение."
                ]
            }
        )

    # В связанные привычки могут попадать только привычки с признаком приятной
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError(
            {"related_habit": "Связанной может быть только приятная привычка."}
        )

    # У приятной привычки не может быть вознаграждения или связанной привычки
    if is_pleasant and (reward or related_habit):
        raise serializers.ValidationError(
            {
                "non_field_errors": [
                    "У приятной привычки не может быть ни вознаграждения, ни связанной привычки."
                ]
            }
        )

    return attrs
