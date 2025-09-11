"""
Permisos personalizados para la app workspace.
"""
from rest_framework import permissions


class IsOrganizationMember(permissions.BasePermission):
    """
    Permiso para verificar que el usuario es miembro de la organización.
    
    Usado en endpoints W03 - obtener organización por ID.
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario es miembro de la organización."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar membresía activa
        return obj.membership_set.filter(
            user=request.user,
            status='active'
        ).exists()


class CanCreateOrganization(permissions.BasePermission):
    """
    Permiso para crear organizaciones.
    
    Usado en endpoint W01 - crear organización.
    Según especificación: crear = Authenticated
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden crear organizaciones."""
        return request.user.is_authenticated


class CanListOrganizations(permissions.BasePermission):
    """
    Permiso para listar organizaciones.
    
    Usado en endpoint W02 - listar mis organizaciones.
    Según especificación: listar = miembro (owner/admin/editor/viewer)
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden listar organizaciones."""
        return request.user.is_authenticated


class IsProjectMember(permissions.BasePermission):
    """
    Permiso para verificar que el usuario es miembro del proyecto.
    
    Usado en endpoints W06 - obtener proyecto por ID.
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario es miembro del proyecto o de su organización."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar membresía en la organización del proyecto
        return obj.organization.membership_set.filter(
            user=request.user,
            status='active'
        ).exists()


class CanCreateProject(permissions.BasePermission):
    """
    Permiso para crear proyectos.
    
    Usado en endpoint W04 - crear proyecto.
    Según especificación: crear = miembro de la org (owner/admin/editor)
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden crear proyectos."""
        return request.user.is_authenticated


class CanListProjects(permissions.BasePermission):
    """
    Permiso para listar proyectos.
    
    Usado en endpoint W05 - listar proyectos de una org.
    Según especificación: leer = miembro de la org
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden listar proyectos."""
        return request.user.is_authenticated
