"""
Trabajo de generación de código.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, JobStatus


class GenerationJob(BaseUUIDModel):
    """Ejecución de generación vinculada a una versión exacta."""
    project = models.ForeignKey(
        'workspace.Project',
        on_delete=models.RESTRICT,
        help_text="Proyecto para el cual se genera código"
    )
    diagram_version = models.ForeignKey(
        'modeling.DiagramVersion',
        on_delete=models.RESTRICT,
        help_text="Versión específica del diagrama a usar"
    )
    template = models.ForeignKey(
        'generation.Template',
        on_delete=models.RESTRICT,
        help_text="Plantilla de generación utilizada"
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que solicitó la generación"
    )
    status = models.CharField(
        max_length=16,
        choices=JobStatus.choices,
        help_text="Estado actual del trabajo"
    )
    started_at = models.DateTimeField(
        help_text="Momento de inicio del trabajo"
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Momento de finalización del trabajo"
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        help_text="Mensaje de error si la generación falló"
    )
    output_path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Ruta del código generado"
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Metadatos del proceso de generación"
    )
    metrics = models.JSONField(
        null=True,
        blank=True,
        help_text="Métricas del proceso de generación"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del trabajo"
    )

    class Meta:
        app_label = 'generation'
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['diagram_version']),
        ]

    def __str__(self):
        return f"Job {self.id} for {self.project.name}"
