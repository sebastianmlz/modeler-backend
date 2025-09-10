"""
Modelo de Evento de Telemetría.
"""
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from Apps.common.models import BaseUUIDModel


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
        app_label = 'telemetry'
        indexes = [
            models.Index(fields=['type', 'ts']),
            models.Index(fields=['project', 'ts']),
            GinIndex(fields=['payload']),
        ]

    def __str__(self):
        return f"{self.type} at {self.ts}"
