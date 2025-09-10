"""
Modelo de Proyecto.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, TimeStampedModel, SoftDeleteModel


class Project(BaseUUIDModel, TimeStampedModel, SoftDeleteModel):
    """Contenedor de diagramas y generación para una organización."""
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.RESTRICT,
        help_text="Organización propietaria del proyecto"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre del proyecto"
    )
    key = models.CharField(
        max_length=16,
        help_text="Clave corta del proyecto"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Descripción del proyecto"
    )
    is_private = models.BooleanField(
        default=False,
        help_text="Si el proyecto es privado"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó el proyecto"
    )

    class Meta:
        app_label = 'workspace'
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'key'],
                name='unique_organization_project_key'
            )
        ]
        indexes = [
            models.Index(fields=['organization']),
        ]

    def __str__(self):
        return f"{self.organization.name}/{self.key}"
