from rest_framework.permissions import BasePermission

from authenticate.models import User


class WorkerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != User.RoleType.EMPLOYER:
            return True
        return False
