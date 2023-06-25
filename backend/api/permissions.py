from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Класс доступа для автора поста."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс доступа для администрации сайта."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )
