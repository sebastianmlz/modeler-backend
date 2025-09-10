"""
Plantilla de generación de código.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel


class Template(BaseUUIDModel):
    """Plantilla de generación de código."""
    name = models.CharField(
        max_length=120,
        help_text="Nombre de la plantilla"
    )
    language_target = models.CharField(
        max_length=32,
        help_text="Lenguaje/framework objetivo (ej. SPRING_BOOT)"
    )
    version = models.CharField(
        max_length=20,
        help_text="Versión de la plantilla"
    )
    config = models.JSONField(
        help_text="Configuración de la plantilla"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la plantilla"
    )

    class Meta:
        app_label = 'generation'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'language_target', 'version'],
                name='unique_template_name_lang_version'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.language_target} v{self.version})"
