"""
Modelo de Método.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel, VisibilityKind
from .model_class import ModelClass


class ModelMethod(BaseUUIDModel):
    """Firma de método para representación y documentación."""
    model_class = models.ForeignKey(
        ModelClass,
        on_delete=models.CASCADE,
        help_text="Clase que contiene el método"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre del método"
    )
    return_type = models.CharField(
        max_length=120,
        help_text="Tipo de retorno del método"
    )
    visibility = models.CharField(
        max_length=10,
        choices=VisibilityKind.choices,
        help_text="Visibilidad del método"
    )
    parameters = models.JSONField(
        help_text="Parámetros del método en formato JSON"
    )
    position = models.IntegerField(
        help_text="Posición dentro de la clase"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del método"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.UniqueConstraint(
                fields=['model_class', 'name'],
                name='unique_class_method_name'
            )
        ]

    def __str__(self):
        return f"{self.model_class.name}.{self.name}()"
