"""Сериализаторы приложения accounts.
Содержит сериализатор для регистрации пользователя с валидацией пароля
по встроенным правилам Django."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный сериализатор для получения JWT токенов с использованием email вместо username."""

    username_field = User.USERNAME_FIELD


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя.
    Поля: email, password. Пароль проходит проверку через
    validate_password и сохраняется в хэшированном виде."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def validate_password(self, value):
        """Проверяет пароль на соответствие политике сложности Django."""
        validate_password(value)
        return value

    def create(self, validated_data):
        """Создаёт пользователя и устанавливает хэш пароля."""
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
