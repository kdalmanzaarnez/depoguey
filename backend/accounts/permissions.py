from rest_framework.permissions import BasePermission

from .roles import get_role


class HasWmsRole(BasePermission):
    message = 'Deze actie is alleen beschikbaar voor medewerkers en admins.'

    def has_permission(self, request, view):
        return get_role(request.user) in ('employee', 'admin')


class IsAdminRole(BasePermission):
    message = 'Alleen een admin mag dit doen.'

    def has_permission(self, request, view):
        return get_role(request.user) == 'admin'
