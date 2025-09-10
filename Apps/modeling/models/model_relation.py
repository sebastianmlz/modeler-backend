"""
Modelo de Relación entre Clases.
"""
from django.db import models
from django.db.models import Q
from Apps.common.models import BaseUUIDModel, TimeStampedModel, RelationKind
from .diagram import Diagram
from .model_class import ModelClass


class ModelRelation(BaseUUIDModel, TimeStampedModel):
    """Relación entre clases (asociación, agregación, composición, herencia)."""
    diagram = models.ForeignKey(
        Diagram,
        on_delete=models.RESTRICT,
        help_text="Diagrama que contiene la relación"
    )
    source_class = models.ForeignKey(
        ModelClass,
        on_delete=models.RESTRICT,
        related_name='outgoing_relations',
        help_text="Clase origen de la relación"
    )
    target_class = models.ForeignKey(
        ModelClass,
        on_delete=models.RESTRICT,
        related_name='incoming_relations',
        help_text="Clase destino de la relación"
    )
    name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        help_text="Nombre de la relación"
    )
    relation_kind = models.CharField(
        max_length=12,
        choices=RelationKind.choices,
        help_text="Tipo de relación UML"
    )
    source_multiplicity = models.CharField(
        max_length=16,
        help_text="Multiplicidad del lado origen"
    )
    target_multiplicity = models.CharField(
        max_length=16,
        help_text="Multiplicidad del lado destino"
    )
    source_role = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Rol del lado origen"
    )
    target_role = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Rol del lado destino"
    )
    is_bidirectional = models.BooleanField(
        default=False,
        help_text="Si la relación es bidireccional"
    )

    class Meta:
        app_label = 'modeling'
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(relation_kind=RelationKind.INHERITANCE, name__isnull=True, is_bidirectional=False) |
                    ~Q(relation_kind=RelationKind.INHERITANCE)
                ),
                name='inheritance_rules'
            )
        ]
        indexes = [
            models.Index(fields=['diagram']),
            models.Index(fields=['source_class']),
            models.Index(fields=['target_class']),
        ]

    def __str__(self):
        return f"{self.source_class.name} -> {self.target_class.name} ({self.relation_kind})"
