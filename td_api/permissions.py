from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            else:
                return obj.owner == request.user
        else:
            return False
