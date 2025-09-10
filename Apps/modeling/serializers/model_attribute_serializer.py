"""
Serializer para el modelo ModelAttribute.
"""
from rest_framework import serializers
from ..models import ModelAttribute


class ModelAttributeSerializer(serializers.ModelSerializer):
    """Serializer para atributos de clase."""
    
    class Meta:
        model = ModelAttribute
        fields = [
            'id',
            'model_class',
            'name',
            'type_name',
            'is_required',
            'is_primary_key',
            'length',
            'precision',
            'scale',
            'default_value',
            'visibility',
            'position',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
