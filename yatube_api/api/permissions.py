from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Предоставляет разрешения на доступ."""
    def has_object_permission(self, request, view, obj):
        # Разрешение на изменение объекта предоставляется только если
        # текущий пользователь является автором объекта.
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class ReadOnly(permissions.BasePermission):
    """Предоставляет разрешение только читать данные."""
    def has_permission(self, request, view):
        # Разрешение предоставляется, если метод запроса является безопасным.
        return request.method in permissions.SAFE_METHODS
