"""
Modelos base abstractos para el sistema de modelado colaborativo.
"""
import uuid
from django.db import models


class BaseUUIDModel(models.Model):
    """Base con identificador UUID como clave primaria."""
    id = models.UUIDField(
        default=uuid.uuid4, 
        primary_key=True, 
        help_text="Identificador único universal"
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """Marca de tiempos de creación y actualización."""
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de última actualización"
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Soporte para borrado lógico mediante marca de tiempo."""
    deleted_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Fecha y hora de borrado lógico"
    )

    class Meta:
        abstract = True
