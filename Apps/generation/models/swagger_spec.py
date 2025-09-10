"""
Especificación Swagger/OpenAPI.
"""
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from Apps.common.models import BaseUUIDModel


class SwaggerSpec(BaseUUIDModel):
    """Especificación OpenAPI generada para el proyecto."""
    job = models.OneToOneField(
        'generation.GenerationJob',
        on_delete=models.CASCADE,
        help_text="Trabajo que generó esta especificación"
    )
    spec_json = models.JSONField(
        help_text="Especificación OpenAPI en formato JSON"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la especificación"
    )

    class Meta:
        app_label = 'generation'
        indexes = [
            GinIndex(fields=['spec_json']),
        ]

    def __str__(self):
        return f"Swagger for job {self.job.id}"
