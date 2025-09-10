"""
ViewSets para telemetría del sistema.
"""
from rest_framework import viewsets, permissions
from ..models import Event, AuditLog, UsageStat, ErrorLog
from ..serializers import EventSerializer, AuditLogSerializer, UsageStatSerializer, ErrorLogSerializer


class EventViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar eventos de telemetría."""
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar eventos por acceso del usuario."""
        user = self.request.user
        if user.is_superuser:
            return Event.objects.all()
        
        # Solo eventos relacionados con proyectos accesibles
        return Event.objects.filter(
            project__organization__membership__user=user,
            project__organization__membership__status='active'
        )


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
