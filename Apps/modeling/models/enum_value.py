"""
Modelo de Valor de Enumeración.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel
from .enum_type import EnumType


class EnumValue(BaseUUIDModel):
    """Valor dentro del enum."""
    enum_type = models.ForeignKey(
        EnumType,
        on_delete=models.CASCADE,
        help_text="Tipo enumerado que contiene este valor"
    )
    literal = models.CharField(
        max_length=120,
        help_text="Literal del valor enumerado"
    )
    ordinal = models.IntegerField(
        help_text="Posición ordinal dentro del enum"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del valor"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.UniqueConstraint(
                fields=['enum_type', 'literal'],
                name='unique_enum_literal'
            )
        ]

    def __str__(self):
        return f"{self.enum_type.name}.{self.literal}"
