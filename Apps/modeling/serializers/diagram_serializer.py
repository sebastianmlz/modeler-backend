"""
Serializer para el modelo Diagram.
"""
from rest_framework import serializers
from ..models import Diagram


class DiagramSerializer(serializers.ModelSerializer):
    """Serializer para diagramas."""
    
    class Meta:
        model = Diagram
        fields = [
            'id',
            'project',
            'name',
            'current_version',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
