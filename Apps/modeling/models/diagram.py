"""
Modelo de Diagrama.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, TimeStampedModel, SoftDeleteModel


class Diagram(BaseUUIDModel, TimeStampedModel, SoftDeleteModel):
    """Diagrama activo dentro de un proyecto."""
    project = models.ForeignKey(
        'workspace.Project',
        on_delete=models.RESTRICT,
        help_text="Proyecto que contiene el diagrama"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre del diagrama"
    )
    current_version = models.ForeignKey(
        'DiagramVersion',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name='current_for_diagrams',
        help_text="Versión actual del diagrama"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó el diagrama"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'name'],
                name='unique_project_diagram_name'
            )
        ]
        indexes = [
            models.Index(fields=['project']),
        ]

    def __str__(self):
        return f"{self.project.name}/{self.name}"
