"""
Serializer para el modelo EnumType.
"""
from rest_framework import serializers
from ..models import EnumType


class EnumTypeSerializer(serializers.ModelSerializer):
    """Serializer para tipos enumerados."""
    
    class Meta:
        model = EnumType
        fields = [
            'id',
            'diagram',
            'name',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
