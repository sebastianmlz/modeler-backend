"""
Modelo de ErrorLog.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel


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
        app_label = 'telemetry'
        indexes = [
            models.Index(fields=['scope', 'ts']),
        ]

    def __str__(self):
        return f"[{self.scope}] {self.message[:50]}..."
