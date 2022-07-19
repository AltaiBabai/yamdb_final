from rest_framework import permissions


class ReadOnlyOrAdmins(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_anonymous
                and request.method not in permissions.SAFE_METHODS):
            return False
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin)


class ReadOnlyOrOwnerOrAllAdmins(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.user.is_anonymous
                and request.method not in permissions.SAFE_METHODS):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user)


class OwnerOrAdmins(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            request.user.is_anonymous
            or not (
                request.user.is_admin
                or request.user.is_superuser)):
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return (
            obj.username == request.user
            or request.user.is_admin
            or request.user.is_superuser)
