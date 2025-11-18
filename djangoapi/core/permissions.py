from rest_framework import permissions


class IsApprovedUser(permissions.BasePermission):
    """
    Permiso que requiere que el usuario esté autenticado Y aprobado.
    
    - Usuario debe estar autenticado (is_authenticated=True)
    - Usuario debe estar aprobado (is_approved=True)
    - Superusuarios siempre tienen acceso (se auto-aprueban)
    """
    
    message = "Tu cuenta está pendiente de aprobación por el administrador."
    
    def has_permission(self, request, view):
        # Usuario debe estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superusuarios siempre tienen acceso
        if request.user.is_superuser:
            return True
        
        # Usuario debe estar aprobado
        return request.user.is_approved


class IsSuperUser(permissions.BasePermission):
    """
    Permiso que solo permite acceso a superusuarios.
    """
    
    message = "Solo los administradores pueden realizar esta acción."
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser