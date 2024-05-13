from rest_framework.permissions import BasePermission

class IsEstudianteAuthOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role == 'estudiante':
                return
            if request.method == "GET":
                return True