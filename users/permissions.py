from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):

        if request.method == "POST":
            return True

        if (request.user.is_authenticated and request.user.is_admin) == True:
            return True

        return False


class IsClient(BasePermission):
    def has_permission(self, request, view):

        if request.user.is_authenticated == True and request.user.is_admin == False:
            return True

        return False