"""
Modelo de Membresía.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, TimeStampedModel, OrgRole, MembershipStatus


class Membership(BaseUUIDModel, TimeStampedModel):
    """Pertenencia del usuario a la organización con rol y estado."""
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.RESTRICT,
        help_text="Organización a la que pertenece"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario miembro"
    )
    role = models.CharField(
        max_length=10,
        choices=OrgRole.choices,
        help_text="Rol del usuario en la organización"
    )
    status = models.CharField(
        max_length=10,
        choices=MembershipStatus.choices,
        help_text="Estado de la membresía"
    )

    class Meta:
        app_label = 'workspace'
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'user'],
                name='unique_organization_user'
            )
        ]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} in {self.organization.name}"
