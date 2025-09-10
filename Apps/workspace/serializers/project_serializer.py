"""
Serializer para el modelo Project.
"""
from rest_framework import serializers
from ..models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer para proyectos."""
    
    class Meta:
        model = Project
        fields = [
            'id',
            'organization',
            'name',
            'key',
            'description',
            'is_private',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_key(self, value):
        """Validar que la clave del proyecto tenga formato correcto."""
        import re
        if not re.match(r'^[A-Z0-9]+$', value):
            raise serializers.ValidationError(
                "La clave del proyecto solo puede contener letras mayúsculas y números."
            )
        if len(value) > 16:
            raise serializers.ValidationError(
                "La clave del proyecto no puede tener más de 16 caracteres."
            )
        return value
