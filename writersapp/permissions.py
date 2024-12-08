from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        print('user token object', request.user.role)
        return request.user.is_authenticated and request.user.role == 'admin'
