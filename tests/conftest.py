import os
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


# Use fast in-memory SQLite DB for tests to avoid external Postgres dependency
@pytest.fixture(scope="session")
def django_db_setup():
    from django.conf import settings as dj_settings
    dj_settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": False,
    }


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def user(db):
    return User.objects.create_user(username="u1", password="pass12345")


@pytest.fixture()
def user2(db):
    return User.objects.create_user(username="u2", password="pass12345")


@pytest.fixture()
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture()
def auth_client2(user2):
    client = APIClient()
    client.force_authenticate(user=user2)
    return client
