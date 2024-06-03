from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Verifica si el usuario es un superusuario (administrador)
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Verifica si el usuario es un superusuario (administrador)
        if request.user.is_superuser:
            return True
        return False
