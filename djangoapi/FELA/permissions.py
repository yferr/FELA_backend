from rest_framework import permissions


class DeleteOnlySuperuser(permissions.BasePermission):
    """
    Permiso custom:
    - GET (list, retrieve): Cualquier usuario (incluso anónimos)
    - POST, PUT, PATCH: Usuario autenticado
    - DELETE: Solo superusuarios
    """

    def has_permission(self, request, view):
        # Permitir lectura a cualquiera
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para crear/actualizar, debe estar autenticado
        if request.method in ['POST', 'PUT', 'PATCH']:
            return request.user and request.user.is_authenticated
        
        # Para eliminar, debe ser superusuario
        if request.method == 'DELETE':
            return request.user and request.user.is_superuser
        
        return False


class IsSuperuserPermission(permissions.BasePermission):
    """
    Permiso que solo permite acceso a superusuarios.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser