"""
Modelo de Comentario.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, SoftDeleteModel


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
        app_label = 'collaboration'
        indexes = [
            models.Index(fields=['diagram', 'target_type', 'target_id']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.target_type}"
