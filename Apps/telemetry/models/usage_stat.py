"""
Modelo de UsageStat.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel


class UsageStat(BaseUUIDModel):
    """Agregados de métricas por día/proyecto."""
    date = models.DateField(
        help_text="Fecha de la métrica"
    )
    project = models.ForeignKey(
        'workspace.Project',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        help_text="Proyecto asociado (opcional para métricas globales)"
    )
    metric_name = models.CharField(
        max_length=64,
        help_text="Nombre de la métrica"
    )
    metric_value = models.BigIntegerField(
        help_text="Valor de la métrica"
    )

    class Meta:
        app_label = 'telemetry'
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'project', 'metric_name'],
                name='unique_daily_project_metric'
            )
        ]

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} on {self.date}"
