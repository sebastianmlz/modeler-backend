"""
Modelo de AuditLog.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel


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
        app_label = 'telemetry'
        indexes = [
            models.Index(fields=['entity_type', 'entity_id', 'ts']),
        ]

    def __str__(self):
        return f"{self.action} {self.entity_type} {self.entity_id}"
