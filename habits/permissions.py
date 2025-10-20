"""Права доступа для домена привычек."""

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Разрешает доступ только владельцу экземпляра модели."""

    message = "Доступ разрешён только владельцу объекта."

    def has_object_permission(self, request, view, obj):
        """Проверяет, совпадает ли пользователь запроса с владельцем объекта."""
        return getattr(obj, "user_id", None) == getattr(request.user, "id", None)
