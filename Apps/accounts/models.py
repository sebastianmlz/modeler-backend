"""
Modelos relacionados con perfiles de usuario.
"""
from django.conf import settings
from django.db import models
from common.models import BaseUUIDModel, TimeStampedModel


class UserProfile(BaseUUIDModel, TimeStampedModel):
    """Metadatos visuales y de preferencia del usuario."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        unique=True,
        help_text="Usuario asociado al perfil"
    )
    display_name = models.CharField(
        max_length=120,
        help_text="Nombre para mostrar en la interfaz"
    )
    avatar_url = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        help_text="URL del avatar del usuario"
    )
    locale = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        help_text="Configuración regional del usuario"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='unique_user_profile'
            )
        ]
        
    def __str__(self):
        return f"Profile for {self.user.username}"
