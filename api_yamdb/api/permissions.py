from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated and user.is_admin or user.is_superuser:
            return True
        return False


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_admin or user.is_superuser


class IsModeratorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_moderator


class IsAuthorOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.author