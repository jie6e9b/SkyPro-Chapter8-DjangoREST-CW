"""Представления для работы с привычками.
Содержит ViewSet для CRUD собственных привычек и список публичных привычек.
"""

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Habit
from .permissions import IsOwner
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек текущего пользователя."""

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Возвращает только привычки текущего пользователя."""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Автоматически проставляет владельца привычки."""
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Ограничивает доступ к объектам только владельцу."""
        if self.action in ["list", "create", "retrieve", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()


class PublicHabitListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Публичный список привычек (без авторизации)."""

    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """Возвращает список только публичных привычек."""
        return super().list(request, *args, **kwargs)
