import os
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# Ensure tests use SQLite settings override
os.environ.setdefault("PYTEST_CURRENT_TEST", "1")


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
