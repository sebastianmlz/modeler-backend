"""
ViewSets para telemetría del sistema.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from ..models import Event, AuditLog, UsageStat, ErrorLog
from ..serializers import EventSerializer, EventListSerializer, AuditLogSerializer, UsageStatSerializer, ErrorLogSerializer


@extend_schema_view(
    create=extend_schema(
        summary="T01 - Registrar evento de telemetría",
        description="Registra un nuevo evento de actividad del usuario en el sistema.",
        responses={201: EventSerializer}
    ),
    list=extend_schema(
        summary="T02 - Listar eventos de telemetría",
        description="Lista eventos de telemetría con filtros opcionales.",
        responses={200: EventListSerializer(many=True)}
    ),
)
class EventViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar eventos de telemetría (T01-T02)."""
    
    queryset = Event.objects.all().order_by('-ts')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'project', 'organization']
    
    def get_serializer_class(self):
        """Usar serializer específico para listado."""
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer
    
    def get_queryset(self):
        """Filtrar eventos por acceso del usuario."""
        user = self.request.user
        queryset = Event.objects.all().order_by('-ts')
        
        if user.is_superuser:
            return queryset
        
        # Filtrar por proyectos/organizaciones accesibles al usuario
        accessible_filters = Q(
            project__organization__membership__user=user,
            project__organization__membership__status='active'
        ) | Q(user=user)  # También eventos propios del usuario
        
        return queryset.filter(accessible_filters).distinct()
    
    def perform_create(self, serializer):
        """T01 - Asignar usuario actual al crear evento."""
        # Si no se especifica usuario, usar el actual
        if 'user' not in serializer.validated_data or not serializer.validated_data['user']:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para logs de auditoría."""
    
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Solo administradores pueden ver logs de auditoría."""
        user = self.request.user
        if user.is_superuser:
            return AuditLog.objects.all()
        
        # Usuarios normales no pueden ver logs de auditoría
        return AuditLog.objects.none()


class UsageStatViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para estadísticas de uso."""
    
    queryset = UsageStat.objects.all()
    serializer_class = UsageStatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar estadísticas por acceso del usuario."""
        user = self.request.user
        if user.is_superuser:
            return UsageStat.objects.all()
        
        # Solo estadísticas de proyectos accesibles
        return UsageStat.objects.filter(
            project__organization__membership__user=user,
            project__organization__membership__status='active'
        )


class ErrorLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para logs de errores."""
    
    queryset = ErrorLog.objects.all()
    serializer_class = ErrorLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Solo administradores pueden ver logs de errores."""
        user = self.request.user
        if user.is_superuser:
            return ErrorLog.objects.all()
        
        # Usuarios normales no pueden ver logs de errores
        return ErrorLog.objects.none()
