from rest_framework import permissions


class DeleteOnlySuperuser(permissions.BasePermission):
    """
    Permiso custom con niveles diferenciados:
    - GET (list, retrieve): Cualquier usuario (incluso anónimos)
    - POST, PUT, PATCH: Usuario autenticado Y aprobado
    - DELETE: Solo superusuarios
    """

    def has_permission(self, request, view):
        # Permitir lectura a cualquiera (público)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Para crear/actualizar, debe estar autenticado Y aprobado
        if request.method in ['POST', 'PUT', 'PATCH']:
            if not request.user or not request.user.is_authenticated:
                return False
            
            # Superusuarios siempre pueden
            if request.user.is_superuser:
                return True
            
            # Usuarios normales deben estar aprobados
            return getattr(request.user, 'is_approved', False)
        
        # Para eliminar, debe ser superusuario
        if request.method == 'DELETE':
            return request.user and request.user.is_authenticated and request.user.is_superuser
        
        return False