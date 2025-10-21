import pytest
from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_habit_business_rules


@pytest.mark.django_db
def test_validator_valid_case(user):
    # Valid: non-pleasant, no reward/related, duration 60, periodicity 1
    attrs = {
        "is_pleasant": False,
        "duration_seconds": 60,
        "periodicity": 1,
        "reward": "",
        "related_habit": None,
    }
    assert validate_habit_business_rules(attrs) == attrs


@pytest.mark.django_db
def test_validator_duration_too_long():
    with pytest.raises(serializers.ValidationError) as exc:
        validate_habit_business_rules({"duration_seconds": 121})
    assert "duration_seconds" in exc.value.detail


@pytest.mark.django_db
def test_validator_periodicity_out_of_range():
    for bad in (0, 8):
        with pytest.raises(serializers.ValidationError) as exc:
            validate_habit_business_rules({"periodicity": bad})
        assert "periodicity" in exc.value.detail


@pytest.mark.django_db
def test_validator_reward_and_related_together(user):
    pleasant = Habit.objects.create(
        user=user,
        place="p",
        time="09:00",
        action="a",
        is_pleasant=True,
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )
    with pytest.raises(serializers.ValidationError) as exc:
        validate_habit_business_rules({"related_habit": pleasant, "reward": "tea"})
    assert "non_field_errors" in exc.value.detail


@pytest.mark.django_db
def test_validator_related_must_be_pleasant(user):
    not_pleasant = Habit.objects.create(
        user=user,
        place="p",
        time="09:00",
        action="a2",
        is_pleasant=False,
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )
    with pytest.raises(serializers.ValidationError) as exc:
        validate_habit_business_rules({"related_habit": not_pleasant, "reward": ""})
    assert "related_habit" in exc.value.detail


@pytest.mark.django_db
def test_validator_pleasant_cannot_have_reward_or_related(user):
    pleasant = Habit.objects.create(
        user=user,
        place="p",
        time="10:00",
        action="a3",
        is_pleasant=True,
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )
    # Passing reward when is_pleasant True
    with pytest.raises(serializers.ValidationError) as exc1:
        validate_habit_business_rules({"is_pleasant": True, "reward": "gift"})
    assert "non_field_errors" in exc1.value.detail

    # Passing related when is_pleasant True
    with pytest.raises(serializers.ValidationError) as exc2:
        validate_habit_business_rules({"is_pleasant": True, "related_habit": pleasant})
    assert "non_field_errors" in exc2.value.detail
