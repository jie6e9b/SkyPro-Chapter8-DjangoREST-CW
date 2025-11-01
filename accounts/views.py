"""Представления (views) для аккаунтов.

Содержит эндпоинт регистрации пользователя.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegistrationSerializer, EmailTokenObtainPairSerializer


class RegisterView(APIView):
    """Регистрация нового пользователя (AllowAny)."""

    permission_classes = [AllowAny]

    @extend_schema(
        request=RegistrationSerializer,
        responses={201: RegistrationSerializer},
    )
    def post(self, request):
        """Принимает email/password и создаёт пользователя."""
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailTokenObtainPairView(TokenObtainPairView):
    """Кастомное view для получения JWT токенов с использованием email вместо username."""

    serializer_class = EmailTokenObtainPairSerializer
