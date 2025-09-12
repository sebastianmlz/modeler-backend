"""
Modelo de Lock (bloqueo) para diagramas.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from Apps.common.models import BaseUUIDModel
from Apps.modeling.models import Diagram


class Lock(BaseUUIDModel):
    """
    Bloqueo temporal de un diagrama para edición colaborativa.
    
    Implementa el mecanismo de locks con TTL (Time To Live) según Fase 1.
    """
    
    diagram = models.OneToOneField(
        Diagram,
        on_delete=models.CASCADE,
        help_text="Diagrama bloqueado"
    )
    
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Usuario que posee el bloqueo"
    )
    
    locked_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Momento en que se adquirió el bloqueo"
    )
    
    expires_at = models.DateTimeField(
        help_text="Momento en que expira el bloqueo"
    )
    
    purpose = models.CharField(
        max_length=100,
        default="editing",
        help_text="Propósito del bloqueo (editing, reviewing, etc.)"
    )
    
    class Meta:
        app_label = 'collaboration'
        indexes = [
            models.Index(fields=['diagram']),
            models.Index(fields=['locked_by']),
            models.Index(fields=['expires_at']),
        ]
    
    def save(self, *args, **kwargs):
        """Establece la fecha de expiración automáticamente."""
        if not self.expires_at:
            # TTL por defecto: 30 minutos según Fase 1
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        """Verifica si el bloqueo ha expirado."""
        return timezone.now() > self.expires_at
    
    @property
    def time_remaining(self):
        """Retorna el tiempo restante antes de la expiración."""
        if self.is_expired:
            return timedelta(0)
        return self.expires_at - timezone.now()
    
    def extend_lock(self, minutes=30):
        """Extiende el bloqueo por los minutos especificados."""
        self.expires_at = timezone.now() + timedelta(minutes=minutes)
        self.save(update_fields=['expires_at'])
    
    def __str__(self):
        return f"Lock on {self.diagram.name} by {self.locked_by.username}"
    
    @classmethod
    def cleanup_expired_locks(cls):
        """Limpia automáticamente los bloqueos expirados."""
        expired_count = cls.objects.filter(expires_at__lt=timezone.now()).delete()[0]
        return expired_count