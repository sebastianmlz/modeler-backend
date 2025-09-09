"""
Modelos base y enumeraciones compartidas para el sistema de modelado colaborativo.
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


class OrgRole(models.TextChoices):
    """Roles dentro de una organización."""
    OWNER = 'OWNER', 'Propietario'
    ADMIN = 'ADMIN', 'Administrador'
    EDITOR = 'EDITOR', 'Editor'
    VIEWER = 'VIEWER', 'Visualizador'


class MembershipStatus(models.TextChoices):
    """Estado de la membresía a una organización."""
    INVITED = 'INVITED', 'Invitado'
    ACTIVE = 'ACTIVE', 'Activo'


class ProjectRole(models.TextChoices):
    """Roles dentro de un proyecto específico."""
    OWNER = 'OWNER', 'Propietario'
    ADMIN = 'ADMIN', 'Administrador'
    EDITOR = 'EDITOR', 'Editor'
    VIEWER = 'VIEWER', 'Visualizador'


class RelationKind(models.TextChoices):
    """Tipos de relaciones UML entre clases."""
    ASSOCIATION = 'ASSOCIATION', 'Asociación'
    AGGREGATION = 'AGGREGATION', 'Agregación'
    COMPOSITION = 'COMPOSITION', 'Composición'
    INHERITANCE = 'INHERITANCE', 'Herencia'


class JobStatus(models.TextChoices):
    """Estados de un trabajo de generación de código."""
    QUEUED = 'QUEUED', 'En cola'
    RUNNING = 'RUNNING', 'Ejecutando'
    SUCCEEDED = 'SUCCEEDED', 'Exitoso'
    FAILED = 'FAILED', 'Fallido'


class ArtifactKind(models.TextChoices):
    """Tipos de artefactos generados por el sistema."""
    ZIP_BACKEND = 'ZIP_BACKEND', 'Backend comprimido'
    SWAGGER_JSON = 'SWAGGER_JSON', 'Especificación Swagger JSON'
    SWAGGER_YAML = 'SWAGGER_YAML', 'Especificación Swagger YAML'
    SQL_SCRIPTS = 'SQL_SCRIPTS', 'Scripts SQL'


class VisibilityKind(models.TextChoices):
    """Niveles de visibilidad para elementos UML."""
    PUBLIC = 'PUBLIC', 'Público'
    PRIVATE = 'PRIVATE', 'Privado'
    PROTECTED = 'PROTECTED', 'Protegido'
    PACKAGE = 'PACKAGE', 'Paquete'
