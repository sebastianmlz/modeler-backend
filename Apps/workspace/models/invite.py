"""
Modelo de Invitación.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, OrgRole


class Invite(BaseUUIDModel):
    """Invitaciones por correo a la organización."""
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.RESTRICT,
        help_text="Organización que envía la invitación"
    )
    email = models.CharField(
        max_length=255,
        help_text="Correo del usuario invitado"
    )
    role = models.CharField(
        max_length=10,
        choices=OrgRole.choices,
        help_text="Rol propuesto para el invitado"
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        help_text="Token único de la invitación"
    )
    expires_at = models.DateTimeField(
        help_text="Fecha de expiración de la invitación"
    )
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Usuario que aceptó la invitación"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la invitación"
    )

    class Meta:
        app_label = 'workspace'

    def __str__(self):
        return f"Invite {self.email} to {self.organization.name}"
