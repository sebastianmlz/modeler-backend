"""
Serializer para Presence.
"""
from rest_framework import serializers
from ..models import Presence


class PresenceSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Presence."""
    
    class Meta:
        model = Presence
        fields = '__all__'
        read_only_fields = ['id']
