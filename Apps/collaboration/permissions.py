"""
Permisos personalizados para la app collaboration.
"""
from rest_framework import permissions
from Apps.workspace.models import ProjectMember


class CanCreateLock(permissions.BasePermission):
    """
    Permiso para crear bloqueos en diagramas.
    
    Usado en endpoint C01 - crear bloqueo.
    Según especificación: cualquier miembro del proyecto puede crear bloqueos.
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden crear bloqueos."""
        return request.user.is_authenticated


class CanViewLock(permissions.BasePermission):
    """
    Permiso para ver bloqueos.
    
    Usado en endpoints C02, C03 - listar y obtener bloqueos.
    Según especificación: cualquier miembro del proyecto puede ver bloqueos.
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario puede ver el bloqueo."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar membresía en la organización del proyecto
        return obj.diagram.project.organization.membership_set.filter(
            user=request.user,
            status='active'
        ).exists()


class CanReleaseLock(permissions.BasePermission):
    """
    Permiso para liberar bloqueos.
    
    Usado en endpoint C04 - liberar bloqueo.
    Según especificación: solo el propietario del bloqueo o admin+ puede liberarlo.
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario puede liberar el bloqueo."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # El propietario del bloqueo puede liberarlo
        if obj.locked_by == request.user:
            return True
            
        # Admins y owners de la organización pueden liberar cualquier bloqueo
        return obj.diagram.project.organization.membership_set.filter(
            user=request.user,
            status='active',
            role__in=['owner', 'admin']
        ).exists()


class CanExtendLock(permissions.BasePermission):
    """
    Permiso para extender bloqueos.
    
    Usado para extender la duración de un bloqueo.
    Según especificación: solo el propietario del bloqueo puede extenderlo.
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario puede extender el bloqueo."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Solo el propietario del bloqueo puede extenderlo
        return obj.locked_by == request.user


class CanListLocks(permissions.BasePermission):
    """
    Permiso para listar bloqueos.
    
    Usado en endpoint C02 - listar bloqueos del proyecto.
    Según especificación: cualquier miembro del proyecto puede listar bloqueos.
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden listar bloqueos."""
        return request.user.is_authenticated