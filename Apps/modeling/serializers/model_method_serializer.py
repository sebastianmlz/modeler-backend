"""
Serializer para el modelo ModelMethod.
"""
from rest_framework import serializers
from ..models import ModelMethod


class ModelMethodSerializer(serializers.ModelSerializer):
    """Serializer para métodos de clase."""
    
    class Meta:
        model = ModelMethod
        fields = [
            'id',
            'model_class',
            'name',
            'return_type',
            'visibility',
            'parameters',
            'position',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
