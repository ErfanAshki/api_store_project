from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS : 
            return True
        return bool(request.user and request.user.is_staff)
 

class SendPrivateEmailToCustomers(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('shop.send_private_email'))

