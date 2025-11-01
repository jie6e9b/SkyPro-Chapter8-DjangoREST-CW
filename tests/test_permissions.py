import pytest
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from habits.permissions import IsOwner
from habits.models import Habit


@pytest.mark.django_db
def test_is_owner_allows_owner(user):
    habit = Habit.objects.create(
        user=user,
        place="home",
        time="08:00:00",
        action="read",
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )
    factory = APIRequestFactory()
    drf_request = Request(factory.get("/"))
    drf_request.user = user

    perm = IsOwner()
    assert perm.has_object_permission(drf_request, view=None, obj=habit) is True


@pytest.mark.django_db
def test_is_owner_denies_other_user(user, user2):
    habit = Habit.objects.create(
        user=user,
        place="home",
        time="08:00:00",
        action="read",
        duration_seconds=60,
        periodicity=1,
        is_public=False,
    )
    factory = APIRequestFactory()
    drf_request = Request(factory.get("/"))
    drf_request.user = user2

    perm = IsOwner()
    assert perm.has_object_permission(drf_request, view=None, obj=habit) is False
