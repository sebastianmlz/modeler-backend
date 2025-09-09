"""
Modelos para organizaciones, proyectos y gestión de membresías.
"""
from django.conf import settings
from django.db import models
from common.models import (
    BaseUUIDModel, TimeStampedModel, SoftDeleteModel,
    OrgRole, MembershipStatus, ProjectRole
)


class Organization(BaseUUIDModel, TimeStampedModel, SoftDeleteModel):
    """Tenant lógico para aislar proyectos y permisos."""
    name = models.CharField(
        max_length=120,
        help_text="Nombre de la organización"
    )
    slug = models.CharField(
        max_length=80,
        unique=True,
        help_text="Identificador único legible para URLs"
    )
    plan = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        help_text="Plan de suscripción de la organización"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó la organización"
    )

    def __str__(self):
        return self.name


class Membership(BaseUUIDModel, TimeStampedModel):
    """Pertenencia del usuario a la organización con rol y estado."""
    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        help_text="Organización a la que pertenece"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario miembro"
    )
    role = models.CharField(
        max_length=10,
        choices=OrgRole.choices,
        help_text="Rol del usuario en la organización"
    )
    status = models.CharField(
        max_length=10,
        choices=MembershipStatus.choices,
        help_text="Estado de la membresía"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'user'],
                name='unique_organization_user'
            )
        ]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} in {self.organization.name}"


class Invite(BaseUUIDModel):
    """Invitaciones por correo a la organización."""
    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        help_text="Organización que envía la invitación"
    )
    email = models.CharField(
        max_length=255,
        help_text="Correo del usuario invitado"
    )
    role = models.CharField(
        max_length=10,
        choices=OrgRole.choices,
        help_text="Rol propuesto para el invitado"
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        help_text="Token único de la invitación"
    )
    expires_at = models.DateTimeField(
        help_text="Fecha de expiración de la invitación"
    )
    accepted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Usuario que aceptó la invitación"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la invitación"
    )

    def __str__(self):
        return f"Invite {self.email} to {self.organization.name}"


class Project(BaseUUIDModel, TimeStampedModel, SoftDeleteModel):
    """Contenedor de diagramas y generación para una organización."""
    organization = models.ForeignKey(
        Organization,
        on_delete=models.RESTRICT,
        help_text="Organización propietaria del proyecto"
    )
    name = models.CharField(
        max_length=120,
        help_text="Nombre del proyecto"
    )
    key = models.CharField(
        max_length=16,
        help_text="Clave corta del proyecto"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Descripción del proyecto"
    )
    is_private = models.BooleanField(
        default=False,
        help_text="Si el proyecto es privado"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que creó el proyecto"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'key'],
                name='unique_organization_project_key'
            )
        ]
        indexes = [
            models.Index(fields=['organization']),
        ]

    def __str__(self):
        return f"{self.organization.name}/{self.key}"


class ProjectMember(BaseUUIDModel):
    """Rol del usuario dentro de un proyecto."""
    project = models.ForeignKey(
        Project,
        on_delete=models.RESTRICT,
        help_text="Proyecto al que pertenece"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario miembro del proyecto"
    )
    role = models.CharField(
        max_length=10,
        choices=ProjectRole.choices,
        help_text="Rol del usuario en el proyecto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de adición al proyecto"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'user'],
                name='unique_project_user'
            )
        ]
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} in {self.project.name}"
