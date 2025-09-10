"""
Serializer para el modelo ModelClass.
"""
from rest_framework import serializers
from ..models import ModelClass


class ModelClassSerializer(serializers.ModelSerializer):
    """Serializer para clases UML."""
    
    class Meta:
        model = ModelClass
        fields = [
            'id',
            'diagram',
            'name',
            'stereotype',
            'visibility',
            'x',
            'y',
            'width',
            'height',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
