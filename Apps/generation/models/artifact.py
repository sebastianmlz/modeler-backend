"""
Artefacto generado.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel, ArtifactKind


class Artifact(BaseUUIDModel):
    """Artefacto generado (archivo, directorio, etc.)."""
    job = models.ForeignKey(
        'generation.GenerationJob',
        on_delete=models.CASCADE,
        help_text="Trabajo que produjo este artefacto"
    )
    kind = models.CharField(
        max_length=16,
        choices=ArtifactKind.choices,
        help_text="Tipo de artefacto"
    )
    filename = models.CharField(
        max_length=255,
        help_text="Nombre del archivo o directorio"
    )
    storage_ref = models.ForeignKey(
        'generation.StorageRef',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Referencia de almacenamiento"
    )
    content = models.TextField(
        null=True,
        blank=True,
        help_text="Contenido del artefacto (para archivos pequeños)"
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Metadatos adicionales del artefacto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del artefacto"
    )

    class Meta:
        app_label = 'generation'
        indexes = [
            models.Index(fields=['job']),
        ]

    def __str__(self):
        return f"{self.filename} ({self.kind})"
