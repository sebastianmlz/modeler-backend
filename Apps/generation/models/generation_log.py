"""
Log de generación.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel


class GenerationLog(BaseUUIDModel):
    """Bitácora línea a línea del proceso de generación."""
    job = models.ForeignKey(
        'generation.GenerationJob',
        on_delete=models.CASCADE,
        help_text="Trabajo asociado al log"
    )
    level = models.CharField(
        max_length=16,
        help_text="Nivel del log (INFO, WARN, ERROR, etc.)"
    )
    message = models.TextField(
        help_text="Mensaje del log"
    )
    ts = models.DateTimeField(
        help_text="Timestamp del mensaje"
    )

    class Meta:
        app_label = 'generation'
        indexes = [
            models.Index(fields=['job', 'ts']),
        ]

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}..."
