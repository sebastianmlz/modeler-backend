"""
Modelo de Presencia de Usuario.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel


class Presence(BaseUUIDModel):
    """Presencia y puntero del usuario dentro de la sesión."""
    session = models.ForeignKey(
        'CollabSession',
        on_delete=models.RESTRICT,
        help_text="Sesión colaborativa"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario presente en la sesión"
    )
    last_seen_at = models.DateTimeField(
        help_text="Última actividad del usuario"
    )
    cursor = models.JSONField(
        null=True,
        blank=True,
        help_text="Posición del cursor/selección del usuario"
    )

    class Meta:
        app_label = 'collaboration'
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'user'],
                name='unique_session_user_presence'
            )
        ]

    def __str__(self):
        return f"{self.user.username} in {self.session.diagram.name}"
