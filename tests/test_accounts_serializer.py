import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from accounts.serializers import RegistrationSerializer

User = get_user_model()


@pytest.mark.django_db
def test_registration_serializer_creates_user_with_hashed_password():
    data = {"email": "s@example.com", "password": "Str0ngPass!"}
    ser = RegistrationSerializer(data=data)
    assert ser.is_valid(), ser.errors
    user = ser.save()
    assert user.email == "s@example.com"
    # password is hashed in DB
    assert user.password != data["password"]
    assert check_password("Str0ngPass!", user.password)


@pytest.mark.django_db
def test_registration_serializer_weak_password_rejected():
    data = {"email": "w@example.com", "password": "12345"}
    ser = RegistrationSerializer(data=data)
    with pytest.raises(serializers.ValidationError):
        ser.is_valid(raise_exception=True)
