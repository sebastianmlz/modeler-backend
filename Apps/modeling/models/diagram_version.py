"""
Modelo de Versión de Diagrama.
"""
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from Apps.common.models import BaseUUIDModel
from .diagram import Diagram


class DiagramVersion(BaseUUIDModel):
    """Snapshot JSON reproducible del diagrama."""
    diagram = models.ForeignKey(
        Diagram,
        on_delete=models.RESTRICT,
        help_text="Diagrama versionado"
    )
    version_number = models.IntegerField(
        help_text="Número de versión secuencial"
    )
    snapshot = models.JSONField(
        help_text="Estado completo del diagrama en JSON"
    )
    message = models.CharField(
        max_length=240,
        null=True,
        blank=True,
        help_text="Mensaje descriptivo de la versión"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó la versión"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la versión"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.UniqueConstraint(
                fields=['diagram', 'version_number'],
                name='unique_diagram_version_number'
            )
        ]
        indexes = [
            models.Index(fields=['diagram']),
            GinIndex(fields=['snapshot']),
        ]

    def __str__(self):
        return f"{self.diagram.name} v{self.version_number}"
