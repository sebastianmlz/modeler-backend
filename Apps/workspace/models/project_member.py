"""
Modelo de Miembro de Proyecto.
"""
from django.conf import settings
from django.db import models
from Apps.common.models import BaseUUIDModel, ProjectRole
from .project import Project


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
        app_label = 'workspace'
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
