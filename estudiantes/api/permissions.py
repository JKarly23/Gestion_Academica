'''from rest_framework.permissions import BasePermission

def get_permission_students(user):
    permission = set()
    if user.role == "estudiante":
        for group in user.groups.all():
            permission.update(group.permissions.all())
    
    return permission


class PermissionsOfStudents(BasePermission):

    def has_permission(self, request, view):

        user = request.user
        professor_permission = get_permission_students(user)
        requiered_permissions = {'view_nota','view_comentarioasignatura','delete_comentarioasignatura','change_comentarioasignatura','add_comentarioasignatura','view_asignatura', 'view_profesor', 'view_estudiante','view_grupo', 'view_facultad', }

        return requiered_permissions.issubset({perm.codename for perm in professor_permission})

    '''