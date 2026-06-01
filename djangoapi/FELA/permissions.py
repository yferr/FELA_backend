"""
permissions.py

Replaces the old DeleteOnlySuperuser permission with IsOwnerOrSuperuser,
which enforces record-level ownership:

- SAFE_METHODS (GET, HEAD, OPTIONS): public access
- POST: authenticated + approved user
- PUT / PATCH / DELETE:
    - the user who created the record  (obj.created_by == request.user)
    - OR a superuser
"""
from rest_framework import permissions


class IsOwnerOrSuperuser(permissions.BasePermission):
    """
    Object-level permission that restricts write operations to the record
    owner or a superuser.
    """

    def has_permission(self, request, view):
        # Public read access
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write operations require authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Superusers always have access
        if request.user.is_superuser:
            return True

        # Regular users must be approved
        return getattr(request.user, 'is_approved', False)

    def has_object_permission(self, request, view, obj):
        # Read is always allowed (already checked at view level)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Superuser: unrestricted access
        if request.user.is_superuser:
            return True

        # Legacy record (no owner assigned): only superuser can modify
        # This prevents any non-superuser from "claiming" ownerless records.
        if obj.created_by is None:
            return False

        # Only the creator can edit or delete their own record
        return obj.created_by == request.user

# ---------------------------------------------------------------------------
# Keep old class as alias for backward compatibility during transition
# (can be removed once all ViewSets are updated)
# ---------------------------------------------------------------------------

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

DeleteOnlySuperuser = IsOwnerOrSuperuser
