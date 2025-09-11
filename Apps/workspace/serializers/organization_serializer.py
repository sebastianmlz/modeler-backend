"""
Serializer para el modelo Organization.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer para organizaciones según especificación Fase 1.
    
    Endpoints compatibles:
    - W01: POST /api/organizations/ → 201 { id, name, slug, created_at }
    - W02: GET /api/organizations/ → 200 [ … ]
    - W03: GET /api/organizations/{id}/ → 200 { … }
    """
    
    class Meta:
        model = Organization
        fields = [
            'id',
            'name', 
            'slug',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_slug(self, value):
        """Validar que el slug sea único y tenga formato correcto."""
        import re
        
        # Formato correcto: solo letras minúsculas, números y guiones
        if not re.match(r'^[a-z0-9-]+$', value):
            raise serializers.ValidationError(
                "El slug solo puede contener letras minúsculas, números y guiones."
            )
        
        # Verificar unicidad (excluyendo el objeto actual en caso de update)
        queryset = Organization.objects.filter(slug=value)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
            
        if queryset.exists():
            raise serializers.ValidationError(
                "Ya existe una organización con este slug."
            )
            
        return value
