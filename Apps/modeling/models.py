"""
Modelos del núcleo del sistema de modelado UML.
"""
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.postgres.indexes import GinIndex
from common.models import (
    BaseUUIDModel, TimeStampedModel, SoftDeleteModel,
    RelationKind, VisibilityKind
)


class Diagram(BaseUUIDModel, TimeStampedModel, SoftDeleteModel):
    """Diagrama activo dentro de un proyecto."""
    project = models.ForeignKey(
        'workspace.Project',
        on_delete=models.RESTRICT,
        help_text="Proyecto que contiene el diagrama"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre del diagrama"
    )
    current_version = models.ForeignKey(
        'DiagramVersion',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        related_name='current_for_diagrams',
        help_text="Versión actual del diagrama"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó el diagrama"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'name'],
                name='unique_project_diagram_name'
            )
        ]
        indexes = [
            models.Index(fields=['project']),
        ]

    def __str__(self):
        return f"{self.project.name}/{self.name}"


class DiagramVersion(BaseUUIDModel):
    """Snapshot JSON reproducible del diagrama."""
    diagram = models.ForeignKey(
        Diagram,
        on_delete=models.RESTRICT,
        help_text="Diagrama versionado"
    )
    version_number = models.IntegerField(
        help_text="Número de versión secuencial"
    )
    snapshot = models.JSONField(
        help_text="Estado completo del diagrama en JSON"
    )
    message = models.CharField(
        max_length=240,
        null=True,
        blank=True,
        help_text="Mensaje descriptivo de la versión"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó la versión"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la versión"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['diagram', 'version_number'],
                name='unique_diagram_version_number'
            )
        ]
        indexes = [
            models.Index(fields=['diagram']),
            GinIndex(fields=['snapshot']),
        ]

    def __str__(self):
        return f"{self.diagram.name} v{self.version_number}"


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
        constraints = [
            models.UniqueConstraint(
                fields=['model_class', 'name'],
                name='unique_class_method_name'
            )
        ]

    def __str__(self):
        return f"{self.model_class.name}.{self.name}()"


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
        constraints = [
            models.UniqueConstraint(
                fields=['diagram', 'name'],
                name='unique_diagram_enum_name'
            )
        ]

    def __str__(self):
        return f"{self.diagram.name}.{self.name}"


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
        constraints = [
            models.UniqueConstraint(
                fields=['enum_type', 'literal'],
                name='unique_enum_literal'
            )
        ]

    def __str__(self):
        return f"{self.enum_type.name}.{self.literal}"


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
