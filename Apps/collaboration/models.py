"""
Modelos para colaboración en tiempo real y sistema de comentarios.
"""
from django.conf import settings
from django.db import models
from common.models import BaseUUIDModel, SoftDeleteModel


class CollabSession(BaseUUIDModel):
    """Sesión de edición colaborativa en tiempo real."""
    diagram = models.ForeignKey(
        'modeling.Diagram',
        on_delete=models.RESTRICT,
        help_text="Diagrama siendo editado colaborativamente"
    )
    started_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que inició la sesión"
    )
    started_at = models.DateTimeField(
        help_text="Momento de inicio de la sesión"
    )
    ended_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Momento de finalización de la sesión"
    )
    metadata = models.JSONField(
        null=True,
        blank=True,
        help_text="Metadatos adicionales de la sesión"
    )

    def __str__(self):
        return f"Session for {self.diagram.name} by {self.started_by.username}"


class Presence(BaseUUIDModel):
    """Presencia y puntero del usuario dentro de la sesión."""
    session = models.ForeignKey(
        CollabSession,
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
        constraints = [
            models.UniqueConstraint(
                fields=['session', 'user'],
                name='unique_session_user_presence'
            )
        ]

    def __str__(self):
        return f"{self.user.username} in {self.session.diagram.name}"


class Comment(BaseUUIDModel, SoftDeleteModel):
    """Comentarios con hilos, anclados a diagrama o elementos."""
    project = models.ForeignKey(
        'workspace.Project',
        on_delete=models.RESTRICT,
        help_text="Proyecto que contiene el comentario"
    )
    diagram = models.ForeignKey(
        'modeling.Diagram',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Diagrama específico (opcional)"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Autor del comentario"
    )
    body = models.TextField(
        help_text="Contenido del comentario"
    )
    target_type = models.CharField(
        max_length=32,
        help_text="Tipo de elemento al que se ancla"
    )
    target_id = models.UUIDField(
        help_text="ID del elemento al que se ancla"
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Comentario padre (para hilos)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del comentario"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de última actualización"
    )

    class Meta:
        indexes = [
            models.Index(fields=['diagram', 'target_type', 'target_id']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.target_type}"
