"""
Permisos personalizados para la app modeling.
"""
from rest_framework import permissions


class IsProjectMemberForDiagram(permissions.BasePermission):
    """
    Permiso para verificar que el usuario es miembro del proyecto del diagrama.
    
    Usado en endpoints M03 - obtener diagrama por ID.
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario es miembro del proyecto del diagrama."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar membresía en la organización del proyecto
        return obj.project.organization.membership_set.filter(
            user=request.user,
            status='active'
        ).exists()


class CanCreateDiagram(permissions.BasePermission):
    """
    Permiso para crear diagramas.
    
    Usado en endpoint M01 - crear diagrama.
    Según especificación: crear = miembro del proyecto (editor+)
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden crear diagramas."""
        return request.user.is_authenticated


class CanListDiagrams(permissions.BasePermission):
    """
    Permiso para listar diagramas.
    
    Usado en endpoint M02 - listar diagramas del proyecto.
    Según especificación: leer = cualquier miembro del proyecto
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden listar diagramas."""
        return request.user.is_authenticated


class CanEditDiagram(permissions.BasePermission):
    """
    Permiso para editar/eliminar diagramas.
    
    Usado en endpoint M03 - renombrar/eliminar diagrama.
    Según especificación: editar/eliminar = editor+
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario puede editar el diagrama."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar membresía con permisos de edición
        return obj.project.organization.membership_set.filter(
            user=request.user,
            status='active',
            role__in=['owner', 'admin', 'editor']
        ).exists()


class CanCreateDiagramVersion(permissions.BasePermission):
    """
    Permiso para crear versiones de diagramas.
    
    Usado en endpoint M04 - crear versión del diagrama.
    Según especificación: crear versión = editor+
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden crear versiones."""
        return request.user.is_authenticated


class CanViewDiagramVersion(permissions.BasePermission):
    """
    Permiso para ver versiones de diagramas.
    
    Usado en endpoints M05, M06 - listar y obtener versiones.
    Según especificación: leer = cualquier miembro del proyecto
    """
    
    def has_object_permission(self, request, view, obj):
        """Verificar si el usuario puede ver la versión del diagrama."""
        # Superusers siempre tienen acceso
        if request.user.is_superuser:
            return True
            
        # Verificar membresía en la organización del proyecto
        return obj.diagram.project.organization.membership_set.filter(
            user=request.user,
            status='active'
        ).exists()


class CanListDiagramVersions(permissions.BasePermission):
    """
    Permiso para listar versiones de diagramas.
    
    Usado en endpoint M05 - listar versiones del diagrama.
    """
    
    def has_permission(self, request, view):
        """Solo usuarios autenticados pueden listar versiones."""
        return request.user.is_authenticated