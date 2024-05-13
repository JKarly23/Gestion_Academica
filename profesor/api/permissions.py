'''from rest_framework.permissions import BasePermission

def get_permission_professor(user):
    permission = set()
    if user.role == "profesor":
        for group in user.groups.all():
            permission.update(group.permissions.all())
    
    return permission


class PermissionsOfProfessor(BasePermission):

    def has_permission(self, request, view):

        user = request.user
        student_permission = get_permission_professor(user)
        requiered_permissions = {'view_nota','add_nota','change_nota','delete_nota','view_comentarioasignatura','view_asignatura', 'view_profesor', 'view_estudiante','view_grupo', 'view_facultad', }

        return requiered_permissions.issubset({perm.codename for perm in student_permission})

    '''