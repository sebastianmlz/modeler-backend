"""
Modelo de Atributo.
"""
from django.db import models
from django.db.models import Q
from Apps.common.models import BaseUUIDModel, TimeStampedModel, VisibilityKind
from .model_class import ModelClass


class ModelAttribute(BaseUUIDModel, TimeStampedModel):
    """Atributo con tipo y restricciones para generación ORM."""
    model_class = models.ForeignKey(
        ModelClass,
        on_delete=models.CASCADE,
        help_text="Clase que contiene el atributo"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre del atributo"
    )
    type_name = models.CharField(
        max_length=120,
        help_text="Tipo de dato del atributo"
    )
    is_required = models.BooleanField(
        help_text="Si el atributo es obligatorio"
    )
    is_primary_key = models.BooleanField(
        help_text="Si el atributo es clave primaria"
    )
    length = models.IntegerField(
        null=True,
        blank=True,
        help_text="Longitud máxima (para strings)"
    )
    precision = models.IntegerField(
        null=True,
        blank=True,
        help_text="Precisión (para decimales)"
    )
    scale = models.IntegerField(
        null=True,
        blank=True,
        help_text="Escala (para decimales)"
    )
    default_value = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Valor por defecto"
    )
    visibility = models.CharField(
        max_length=10,
        choices=VisibilityKind.choices,
        help_text="Visibilidad del atributo"
    )
    position = models.IntegerField(
        help_text="Posición dentro de la clase"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.UniqueConstraint(
                fields=['model_class', 'name'],
                name='unique_class_attribute_name'
            ),
            models.CheckConstraint(
                check=Q(is_primary_key=False) | Q(is_required=True),
                name='attr_pk_implies_required'
            )
        ]

    def __str__(self):
        return f"{self.model_class.name}.{self.name}"
