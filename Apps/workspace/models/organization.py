"""
Modelo de Organización.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, TimeStampedModel, SoftDeleteModel


class Organization(BaseUUIDModel, TimeStampedModel, SoftDeleteModel):
    """Tenant lógico para aislar proyectos y permisos."""
    name = models.CharField(
        max_length=120,
        help_text="Nombre de la organización"
    )
    slug = models.CharField(
        max_length=80,
        unique=True,
        help_text="Identificador único legible para URLs"
    )
    plan = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Plan de suscripción de la organización"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó la organización"
    )

    class Meta:
        app_label = 'workspace'

    def __str__(self):
        return self.name
