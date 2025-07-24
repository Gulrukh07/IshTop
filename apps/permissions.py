from rest_framework.permissions import BasePermission

from authenticate.models import User


class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role != User.RoleType.WORKER:
            return True
        else:
            return False
