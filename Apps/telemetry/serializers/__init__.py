"""
Serializers para telemetría del sistema.
"""
from rest_framework import serializers
from django.utils import timezone
from ..models import Event, AuditLog, UsageStat, ErrorLog


class EventSerializer(serializers.ModelSerializer):
    """Serializer para crear eventos de telemetría (T01)."""
    
    # Campos de solo lectura para información adicional
    user_username = serializers.CharField(source='user.username', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    diagram_name = serializers.CharField(source='diagram.name', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'type', 'user', 'organization', 'project', 'diagram',
            'payload', 'ts', 'user_username', 'organization_name', 
            'project_name', 'diagram_name'
        ]
        read_only_fields = ['id', 'user_username', 'organization_name', 'project_name', 'diagram_name']
    
    def create(self, validated_data):
        """Crear evento con timestamp automático si no se proporciona."""
        if 'ts' not in validated_data:
            validated_data['ts'] = timezone.now()
        return super().create(validated_data)
    
    def validate_type(self, value):
        """Validar tipos de eventos permitidos."""
        allowed_types = [
            'diagram_created', 'diagram_updated', 'diagram_deleted',
            'version_created', 'project_created', 'user_login',
            'user_logout', 'lock_acquired', 'lock_released'
        ]
        if value not in allowed_types:
            raise serializers.ValidationError(
                f"Tipo de evento no válido. Permitidos: {', '.join(allowed_types)}"
            )
        return value


class EventListSerializer(serializers.ModelSerializer):
    """Serializer para listar eventos de telemetría (T02)."""
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    diagram_name = serializers.CharField(source='diagram.name', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'type', 'user_username', 'organization_name', 
            'project_name', 'diagram_name', 'payload', 'ts'
        ]


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
