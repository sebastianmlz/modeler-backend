"""
Modelos para auditoría, métricas y telemetría del sistema.
"""
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from common.models import BaseUUIDModel


class Event(BaseUUIDModel):
    """Telemetría de uso y acciones del usuario."""
    type = models.CharField(
        max_length=64,
        help_text="Tipo de evento"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Usuario que generó el evento"
    )
    organization = models.ForeignKey(
        'workspace.Organization',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Organización relacionada al evento"
    )
    project = models.ForeignKey(
        'workspace.Project',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Proyecto relacionado al evento"
    )
    diagram = models.ForeignKey(
        'modeling.Diagram',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Diagrama relacionado al evento"
    )
    payload = models.JSONField(
        help_text="Datos adicionales del evento"
    )
    ts = models.DateTimeField(
        help_text="Timestamp del evento"
    )

    class Meta:
        indexes = [
            models.Index(fields=['type', 'ts']),
            models.Index(fields=['project', 'ts']),
            GinIndex(fields=['payload']),
        ]

    def __str__(self):
        return f"{self.type} at {self.ts}"


class AuditLog(BaseUUIDModel):
    """Trazabilidad de cambios críticos."""
    entity_type = models.CharField(
        max_length=32,
        help_text="Tipo de entidad modificada"
    )
    entity_id = models.UUIDField(
        help_text="ID de la entidad modificada"
    )
    action = models.CharField(
        max_length=16,
        help_text="Acción realizada (create/update/delete)"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que realizó la acción"
    )
    before = models.JSONField(
        null=True,
        blank=True,
        help_text="Estado anterior de la entidad"
    )
    after = models.JSONField(
        null=True,
        blank=True,
        help_text="Estado posterior de la entidad"
    )
    ts = models.DateTimeField(
        help_text="Timestamp de la acción"
    )

    class Meta:
        indexes = [
            models.Index(fields=['entity_type', 'entity_id', 'ts']),
        ]

    def __str__(self):
        return f"{self.action} {self.entity_type} {self.entity_id}"


class UsageStat(BaseUUIDModel):
    """Agregados de métricas por día/proyecto."""
    date = models.DateField(
        help_text="Fecha de la métrica"
    )
    project = models.ForeignKey(
        'workspace.Project',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Proyecto asociado (opcional para métricas globales)"
    )
    metric_name = models.CharField(
        max_length=64,
        help_text="Nombre de la métrica"
    )
    metric_value = models.BigIntegerField(
        help_text="Valor de la métrica"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'project', 'metric_name'],
                name='unique_daily_project_metric'
            )
        ]

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} on {self.date}"


class ErrorLog(BaseUUIDModel):
    """Registro centralizado de errores para depuración."""
    scope = models.CharField(
        max_length=32,
        help_text="Ámbito donde ocurrió el error"
    )
    message = models.TextField(
        help_text="Mensaje de error"
    )
    stack = models.TextField(
        null=True,
        blank=True,
        help_text="Stack trace del error"
    )
    context = models.JSONField(
        null=True,
        blank=True,
        help_text="Contexto adicional del error"
    )
    ts = models.DateTimeField(
        help_text="Timestamp del error"
    )

    class Meta:
        indexes = [
            models.Index(fields=['scope', 'ts']),
        ]

    def __str__(self):
        return f"[{self.scope}] {self.message[:50]}..."
