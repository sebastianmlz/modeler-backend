"""
Serializer para CollabSession.
"""
from rest_framework import serializers
from ..models import CollabSession


class CollabSessionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo CollabSession."""
    
    class Meta:
        model = CollabSession
        fields = '__all__'
        read_only_fields = ['id', 'started_at']
