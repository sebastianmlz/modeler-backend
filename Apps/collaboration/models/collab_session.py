"""
Modelo de Sesión de Colaboración.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel


class CollabSession(BaseUUIDModel):
    """Sesión de edición colaborativa en tiempo real."""
    diagram = models.ForeignKey(
        'modeling.Diagram',
        on_delete=models.RESTRICT,
        help_text="Diagrama siendo editado colaborativamente"
    )
    started_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que inició la sesión"
    )
    started_at = models.DateTimeField(
        help_text="Momento de inicio de la sesión"
    )
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Momento de finalización de la sesión"
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Metadatos adicionales de la sesión"
    )

    class Meta:
        app_label = 'collaboration'

    def __str__(self):
        return f"Session for {self.diagram.name} by {self.started_by.username}"
