"""
Modelo de Clase UML.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel, TimeStampedModel, VisibilityKind
from .diagram import Diagram


class ModelClass(BaseUUIDModel, TimeStampedModel):
    """Clase UML con posición en el lienzo."""
    diagram = models.ForeignKey(
        Diagram,
        on_delete=models.RESTRICT,
        help_text="Diagrama que contiene la clase"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre de la clase"
    )
    stereotype = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Estereotipo UML de la clase"
    )
    visibility = models.CharField(
        max_length=10,
        choices=VisibilityKind.choices,
        help_text="Visibilidad de la clase"
    )
    x = models.IntegerField(
        help_text="Posición X en el lienzo"
    )
    y = models.IntegerField(
        help_text="Posición Y en el lienzo"
    )
    width = models.IntegerField(
        help_text="Ancho de la clase en el lienzo"
    )
    height = models.IntegerField(
        help_text="Alto de la clase en el lienzo"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.UniqueConstraint(
                fields=['diagram', 'name'],
                name='unique_diagram_class_name'
            )
        ]
        indexes = [
            models.Index(fields=['diagram']),
        ]

    def __str__(self):
        return f"{self.diagram.name}.{self.name}"
