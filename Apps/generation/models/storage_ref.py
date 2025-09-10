"""
Referencia de almacenamiento de archivos.
"""
from django.db import models
from Apps.common.models import BaseUUIDModel


class StorageRef(BaseUUIDModel):
    """Referencia de almacenamiento de archivos generados."""
    provider = models.CharField(
        max_length=16,
        help_text="Proveedor de almacenamiento (S3, GCS, LOCAL)"
    )
    bucket = models.CharField(
        max_length=128,
        help_text="Bucket o contenedor de almacenamiento"
    )
    object_key = models.CharField(
        max_length=512,
        help_text="Clave o ruta del objeto"
    )
    size_bytes = models.BigIntegerField(
        help_text="Tamaño del archivo en bytes"
    )
    content_type = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        help_text="Tipo MIME del contenido"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la referencia"
    )

    class Meta:
        app_label = 'generation'

    def __str__(self):
        return f"{self.provider}://{self.bucket}/{self.object_key}"
