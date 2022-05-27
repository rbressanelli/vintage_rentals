from rest_framework.permissions import BasePermission
from rest_framework.request import Request

class IsAdmin(BasePermission):
    def has_permission(self, request:Request, view):
        if request.method == 'POST' and (
            request.user.is_anonymous or not request.user.is_admin):
            return False
        return True