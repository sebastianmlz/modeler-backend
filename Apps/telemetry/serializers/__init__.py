"""
Serializers para telemetría del sistema.
"""
from rest_framework import serializers
from ..models import Event, AuditLog, UsageStat, ErrorLog


class EventSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Event."""
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer para el modelo AuditLog."""
    
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['id']


class UsageStatSerializer(serializers.ModelSerializer):
    """Serializer para el modelo UsageStat."""
    
    class Meta:
        model = UsageStat
        fields = '__all__'
        read_only_fields = ['id']


class ErrorLogSerializer(serializers.ModelSerializer):
    """Serializer para el modelo ErrorLog."""
    
    class Meta:
        model = ErrorLog
        fields = '__all__'
        read_only_fields = ['id']
