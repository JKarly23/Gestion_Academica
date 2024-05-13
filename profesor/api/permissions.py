from rest_framework.permissions import BasePermission


class IsAuthProfesorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == "GET":
                return True
            if request.user.role == 'profesor':
                return True 
            
        return False