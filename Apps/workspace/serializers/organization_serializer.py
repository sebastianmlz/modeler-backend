"""
Serializer para el modelo Organization.
"""
from rest_framework import serializers
from ..models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer para organizaciones."""
    
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'slug',
            'plan',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
    
    def validate_slug(self, value):
        """Validar que el slug sea único y tenga formato correcto."""
        import re
        if not re.match(r'^[a-z0-9-]+$', value):
            raise serializers.ValidationError(
                "El slug solo puede contener letras minúsculas, números y guiones."
            )
        return value
