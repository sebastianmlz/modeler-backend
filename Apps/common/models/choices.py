"""
Enumeraciones y opciones constantes para el sistema.
"""
from django.db import models


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
