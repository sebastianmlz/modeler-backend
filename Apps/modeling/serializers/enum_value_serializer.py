"""
Serializer para el modelo EnumValue.
"""
from rest_framework import serializers
from ..models import EnumValue


class EnumValueSerializer(serializers.ModelSerializer):
    """Serializer para valores de enumeración."""
    
    class Meta:
        model = EnumValue
        fields = [
            'id',
            'enum_type',
            'literal',
            'ordinal',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
