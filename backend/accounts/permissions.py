from rest_framework.permissions import BasePermission

from .roles import get_role


class IsAdminRole(BasePermission):
    message = 'Alleen een admin mag dit doen.'

    def has_permission(self, request, view):
        return get_role(request.user) == 'admin'
