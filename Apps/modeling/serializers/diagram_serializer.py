"""
Serializer para el modelo Diagram según especificación Fase 1.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Diagram
from Apps.workspace.models import Project


class DiagramSerializer(serializers.ModelSerializer):
    """
    Serializer para diagramas según especificación Fase 1.
    """
    
    class Meta:
        model = Diagram
        fields = [
            'id',
            'project',
            'name',
            'current_version',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'created_by', 'current_version']
    
    def validate_name(self, value):
        """Validar que el nombre tenga formato correcto."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El nombre del diagrama debe tener al menos 3 caracteres."
            )
        return value.strip()
    
    def validate(self, data):
        """Validar unicidad de (project, name)."""
        project = data.get('project')
        name = data.get('name')
        
        if project and name:
            # Verificar unicidad excluyendo el objeto actual en caso de update
            queryset = Diagram.objects.filter(project=project, name=name)
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
                
            if queryset.exists():
                raise serializers.ValidationError({
                    'name': f'Ya existe un diagrama con el nombre "{name}" en este proyecto.'
                })
        
        return data
    
    def validate_project(self, value):
        """Validar que el usuario tiene permisos en el proyecto."""
        user = self.context['request'].user
        
        # Superusers pueden crear en cualquier proyecto
        if user.is_superuser:
            return value
        
        # Verificar que el usuario es miembro de la organización con permisos de edición
        membership = value.organization.membership_set.filter(
            user=user,
            status='active',
            role__in=['owner', 'admin', 'editor']
        ).first()
        
        if not membership:
            raise serializers.ValidationError(
                "No tienes permisos para crear diagramas en este proyecto."
            )
        
        return value


class DiagramUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar nombre de diagrama (M03 - rename).
    """
    
    class Meta:
        model = Diagram
        fields = ['name']
    
    def validate_name(self, value):
        """Validar que el nombre tenga formato correcto."""
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El nombre del diagrama debe tener al menos 3 caracteres."
            )
        return value.strip()
    
    def validate(self, data):
        """Validar unicidad de (project, name) para update."""
        name = data.get('name')
        
        if name and self.instance:
            # Verificar unicidad excluyendo el objeto actual
            queryset = Diagram.objects.filter(
                project=self.instance.project, 
                name=name
            ).exclude(id=self.instance.id)
                
            if queryset.exists():
                raise serializers.ValidationError({
                    'name': f'Ya existe un diagrama con el nombre "{name}" en este proyecto.'
                })
        
        return data
