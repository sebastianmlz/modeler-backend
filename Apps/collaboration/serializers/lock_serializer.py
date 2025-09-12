"""
Serializers para el sistema de bloqueos (locks).
"""
from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from Apps.collaboration.models import Lock
from Apps.modeling.models import Diagram


class LockSerializer(serializers.ModelSerializer):
    """Serializer para crear y listar bloqueos (C01, C02)."""
    
    diagram_id = serializers.UUIDField(write_only=True, required=True)
    diagram_name = serializers.CharField(source='diagram.name', read_only=True)
    locked_by_username = serializers.CharField(source='locked_by.username', read_only=True)
    project_name = serializers.CharField(source='diagram.project.name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    time_remaining_seconds = serializers.SerializerMethodField()
    
    class Meta:
        model = Lock
        fields = [
            'id', 'diagram_id', 'diagram_name', 'project_name',
            'locked_by', 'locked_by_username', 'locked_at', 'expires_at',
            'purpose', 'is_expired', 'time_remaining_seconds'
        ]
        read_only_fields = [
            'id', 'locked_by', 'locked_at', 'expires_at',
            'diagram_name', 'project_name', 'locked_by_username',
            'is_expired', 'time_remaining_seconds'
        ]
    
    def get_time_remaining_seconds(self, obj):
        """Retorna el tiempo restante en segundos."""
        time_remaining = obj.time_remaining
        return int(time_remaining.total_seconds()) if time_remaining > timedelta(0) else 0
    
    def validate_diagram_id(self, value):
        """Valida que el diagrama exista y pueda ser bloqueado."""
        user = self.context['request'].user
        
        try:
            diagram = Diagram.objects.get(id=value)
        except Diagram.DoesNotExist:
            raise serializers.ValidationError("El diagrama especificado no existe")
        
        # Verificar que el usuario sea miembro de la organización del proyecto
        from Apps.workspace.models import Membership
        if not Membership.objects.filter(
            organization=diagram.project.organization,
            user=user,
            status='active'
        ).exists():
            raise serializers.ValidationError("No tienes permisos para bloquear este diagrama")
        
        # Verificar que el diagrama no esté eliminado
        if diagram.deleted_at is not None:
            raise serializers.ValidationError("No se puede bloquear un diagrama eliminado")
        
        # Verificar que no tenga ya un bloqueo activo
        existing_lock = Lock.objects.filter(diagram=diagram, expires_at__gt=timezone.now()).first()
        if existing_lock:
            if existing_lock.locked_by == user:
                raise serializers.ValidationError("Ya tienes un bloqueo activo en este diagrama")
            else:
                raise serializers.ValidationError(
                    f"El diagrama está bloqueado por {existing_lock.locked_by.username} "
                    f"hasta {existing_lock.expires_at.strftime('%H:%M:%S')}"
                )
        
        return value
    
    def validate_purpose(self, value):
        """Valida el propósito del bloqueo."""
        allowed_purposes = ['editing', 'reviewing', 'testing', 'maintenance']
        if value and value not in allowed_purposes:
            raise serializers.ValidationError(
                f"Propósito no válido. Debe ser uno de: {', '.join(allowed_purposes)}"
            )
        return value or 'editing'
    
    def create(self, validated_data):
        """Crea un nuevo bloqueo con limpieza automática de expirados."""
        diagram_id = validated_data.pop('diagram_id')
        user = self.context['request'].user
        
        # Limpiar bloqueos expirados antes de crear uno nuevo
        Lock.cleanup_expired_locks()
        
        # Obtener el diagrama
        diagram = Diagram.objects.get(id=diagram_id)
        
        # Crear el bloqueo
        lock = Lock.objects.create(
            diagram=diagram,
            locked_by=user,
            **validated_data
        )
        
        return lock


class LockDetailSerializer(serializers.ModelSerializer):
    """Serializer para obtener detalles completos de un bloqueo (C03)."""
    
    diagram_name = serializers.CharField(source='diagram.name', read_only=True)
    diagram_id = serializers.UUIDField(source='diagram.id', read_only=True)
    project_name = serializers.CharField(source='diagram.project.name', read_only=True)
    project_id = serializers.UUIDField(source='diagram.project.id', read_only=True)
    locked_by_username = serializers.CharField(source='locked_by.username', read_only=True)
    locked_by_email = serializers.EmailField(source='locked_by.email', read_only=True)
    organization_name = serializers.CharField(source='diagram.project.organization.name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    time_remaining_seconds = serializers.SerializerMethodField()
    duration_seconds = serializers.SerializerMethodField()
    
    class Meta:
        model = Lock
        fields = [
            'id', 'diagram_id', 'diagram_name', 'project_id', 'project_name',
            'organization_name', 'locked_by', 'locked_by_username', 'locked_by_email',
            'locked_at', 'expires_at', 'purpose', 'is_expired',
            'time_remaining_seconds', 'duration_seconds'
        ]
        read_only_fields = [
            'id', 'diagram_id', 'diagram_name', 'project_id', 'project_name',
            'organization_name', 'locked_by', 'locked_by_username', 'locked_by_email',
            'locked_at', 'expires_at', 'purpose', 'is_expired',
            'time_remaining_seconds', 'duration_seconds'
        ]
    
    def get_time_remaining_seconds(self, obj):
        """Retorna el tiempo restante en segundos."""
        time_remaining = obj.time_remaining
        return int(time_remaining.total_seconds()) if time_remaining > timedelta(0) else 0
    
    def get_duration_seconds(self, obj):
        """Retorna la duración total del bloqueo en segundos."""
        duration = obj.expires_at - obj.locked_at
        return int(duration.total_seconds())


class LockExtendSerializer(serializers.Serializer):
    """Serializer para extender la duración de un bloqueo."""
    
    minutes = serializers.IntegerField(
        min_value=1, 
        max_value=120,  # Máximo 2 horas según Fase 1
        default=30,
        help_text="Minutos para extender el bloqueo (1-120)"
    )
    
    def validate_minutes(self, value):
        """Valida que los minutos estén en el rango permitido."""
        if value < 1 or value > 120:
            raise serializers.ValidationError("Los minutos deben estar entre 1 y 120")
        return value