"""
Serializer para el modelo DiagramVersion.
"""
from rest_framework import serializers
from ..models import DiagramVersion


class DiagramVersionSerializer(serializers.ModelSerializer):
    """Serializer para versiones de diagrama."""
    
    class Meta:
        model = DiagramVersion
        fields = [
            'id',
            'diagram',
            'version_number',
            'snapshot',
            'message',
            'created_by',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']
