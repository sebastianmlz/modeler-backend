"""
Modelo de Tipo Enumerado.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel
from .diagram import Diagram


class EnumType(BaseUUIDModel):
    """Tipo enumerado definido por el usuario."""
    diagram = models.ForeignKey(
        Diagram,
        on_delete=models.RESTRICT,
        help_text="Diagrama que contiene el enum"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre del tipo enumerado"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del enum"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.UniqueConstraint(
                fields=['diagram', 'name'],
                name='unique_diagram_enum_name'
            )
        ]

    def __str__(self):
        return f"{self.diagram.name}.{self.name}"
