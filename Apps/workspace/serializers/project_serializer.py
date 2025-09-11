"""
Serializer para el modelo Project según especificación Fase 1.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Project, Organization


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer para proyectos según especificación Fase 1.
    
    Endpoints compatibles:
    - W04: POST /api/projects/ → 201 { id, organization, name, key, created_at }
    - W05: GET /api/projects/?organization=<uuid> → 200 [ … ]
    - W06: GET /api/projects/{id}/ → 200 { … }
    """
    
    class Meta:
        model = Project
        fields = [
            'id',
            'organization',
            'name', 
            'key',
            'is_private',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_key(self, value):
        """Validar que la clave del proyecto tenga formato correcto."""
        import re
        
        # Formato correcto: solo letras mayúsculas y números
        if not re.match(r'^[A-Z0-9]+$', value):
            raise serializers.ValidationError(
                "La clave del proyecto solo puede contener letras mayúsculas y números."
            )
        
        if len(value) > 16:
            raise serializers.ValidationError(
                "La clave del proyecto no puede tener más de 16 caracteres."
            )
        
        return value
    
    def validate(self, data):
        """Validar unicidad de (organization, key)."""
        organization = data.get('organization')
        key = data.get('key')
        
        if organization and key:
            # Verificar unicidad excluyendo el objeto actual en caso de update
            queryset = Project.objects.filter(organization=organization, key=key)
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)
                
            if queryset.exists():
                raise serializers.ValidationError({
                    'key': f'Ya existe un proyecto con la clave "{key}" en esta organización.'
                })
        
        return data
    
    def validate_organization(self, value):
        """Validar que el usuario tiene permisos en la organización."""
        user = self.context['request'].user
        
        # Superusers pueden crear en cualquier organización
        if user.is_superuser:
            return value
        
        # Verificar que el usuario es miembro con permisos de creación
        membership = value.membership_set.filter(
            user=user,
            status='active',
            role__in=['owner', 'admin', 'editor']
        ).first()
        
        if not membership:
            raise serializers.ValidationError(
                "No tienes permisos para crear proyectos en esta organización."
            )
        
        return value
