from rest_framework.permissions import BasePermission

from authenticate.models import User


class WorkerPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        return request.user.role != User.RoleType.EMPLOYER
