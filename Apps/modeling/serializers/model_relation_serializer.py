"""
Serializer para el modelo ModelRelation.
"""
from rest_framework import serializers
from ..models import ModelRelation


class ModelRelationSerializer(serializers.ModelSerializer):
    """Serializer para relaciones entre clases."""
    
    class Meta:
        model = ModelRelation
        fields = [
            'id',
            'diagram',
            'source_class',
            'target_class',
            'name',
            'relation_kind',
            'source_multiplicity',
            'target_multiplicity',
            'source_role',
            'target_role',
            'is_bidirectional',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
