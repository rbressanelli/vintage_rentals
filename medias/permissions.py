from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, _):
        if request.method in ["POST", "PATCH", "DELETE"] and (
            request.user.is_anonymous or not request.user.is_admin
        ):
            return False
        return True


class IsCustomer(BasePermission):
    def has_permission(self, request: Request, _):
        if request.method == "POST" and (
            request.user.is_anonymous or request.user.is_admin
        ):
            return False
        return True

class IsAdminGetMediaRental(BasePermission):
    def has_permission(self, request:Request, _):
        if request.user.is_anonymous or not request.user.is_admin:
            return False
        return True
