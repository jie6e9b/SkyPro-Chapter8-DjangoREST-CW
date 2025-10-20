"""Сериализаторы приложения accounts.
Содержит сериализатор для регистрации пользователя с валидацией пароля
по встроенным правилам Django."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя.
    Поля: username, email, password. Пароль проходит проверку через
    validate_password и сохраняется в хэшированном виде."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_password(self, value):
        """Проверяет пароль на соответствие политике сложности Django."""
        validate_password(value)
        return value

    def create(self, validated_data):
        """Создаёт пользователя и устанавливает хэш пароля."""
        user = User(username=validated_data["username"], email=validated_data.get("email", ""))
        user.set_password(validated_data["password"])
        user.save()
        return user
