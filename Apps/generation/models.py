"""
Modelos para plantillas, trabajos de generación y artefactos.
"""
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from common.models import BaseUUIDModel, JobStatus, ArtifactKind


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
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'language_target', 'version'],
                name='unique_template_name_lang_version'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.language_target} v{self.version})"


class GenerationJob(BaseUUIDModel):
    """Ejecución de generación vinculada a una versión exacta."""
    project = models.ForeignKey(
        'workspace.Project',
        on_delete=models.RESTRICT,
        help_text="Proyecto para el cual se genera código"
    )
    diagram = models.ForeignKey(
        'modeling.Diagram',
        on_delete=models.RESTRICT,
        help_text="Diagrama base para la generación"
    )
    diagram_version = models.ForeignKey(
        'modeling.DiagramVersion',
        on_delete=models.RESTRICT,
        help_text="Versión específica del diagrama"
    )
    template = models.ForeignKey(
        Template,
        on_delete=models.RESTRICT,
        help_text="Plantilla utilizada para la generación"
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.RESTRICT,
        help_text="Usuario que solicitó la generación"
    )
    status = models.CharField(
        max_length=10,
        choices=JobStatus.choices,
        help_text="Estado del trabajo de generación"
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Momento de inicio de la generación"
    )
    finished_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Momento de finalización"
    )
    metrics = models.JSONField(
        null=True,
        blank=True,
        help_text="Métricas del proceso de generación"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del trabajo"
    )

    class Meta:
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['diagram_version']),
        ]

    def __str__(self):
        return f"Job {self.id} for {self.project.name}"


class StorageRef(BaseUUIDModel):
    """Referencia de almacenamiento de archivos generados."""
    provider = models.CharField(
        max_length=16,
        help_text="Proveedor de almacenamiento"
    )
    bucket = models.CharField(
        max_length=120,
        help_text="Bucket o contenedor"
    )
    object_key = models.CharField(
        max_length=512,
        help_text="Clave del objeto en el almacenamiento"
    )
    url = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        help_text="URL de acceso directo"
    )
    content_type = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text="Tipo MIME del contenido"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la referencia"
    )

    def __str__(self):
        return f"{self.provider}://{self.bucket}/{self.object_key}"


class Artifact(BaseUUIDModel):
    """Archivo resultado, ej. ZIP backend, Swagger JSON/YAML."""
    job = models.ForeignKey(
        GenerationJob,
        on_delete=models.CASCADE,
        help_text="Trabajo que generó el artefacto"
    )
    kind = models.CharField(
        max_length=15,
        choices=ArtifactKind.choices,
        help_text="Tipo de artefacto generado"
    )
    filename = models.CharField(
        max_length=255,
        help_text="Nombre del archivo"
    )
    size_bytes = models.BigIntegerField(
        help_text="Tamaño del archivo en bytes"
    )
    sha256 = models.CharField(
        max_length=64,
        help_text="Hash SHA256 del archivo"
    )
    storage_ref = models.ForeignKey(
        StorageRef,
        on_delete=models.RESTRICT,
        help_text="Referencia de almacenamiento"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del artefacto"
    )

    class Meta:
        indexes = [
            models.Index(fields=['job']),
        ]

    def __str__(self):
        return f"{self.filename} ({self.kind})"


class GenerationLog(BaseUUIDModel):
    """Bitácora línea a línea del proceso de generación."""
    job = models.ForeignKey(
        GenerationJob,
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
        indexes = [
            models.Index(fields=['job', 'ts']),
        ]

    def __str__(self):
        return f"[{self.level}] {self.message[:50]}..."


class SwaggerSpec(BaseUUIDModel):
    """OpenAPI 3 generado para los endpoints del backend."""
    job = models.ForeignKey(
        GenerationJob,
        on_delete=models.RESTRICT,
        help_text="Trabajo que generó la especificación"
    )
    version = models.CharField(
        max_length=16,
        default='3.0',
        help_text="Versión de OpenAPI"
    )
    spec_json = models.JSONField(
        help_text="Especificación OpenAPI en formato JSON"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación de la especificación"
    )

    class Meta:
        indexes = [
            GinIndex(fields=['spec_json']),
        ]

    def __str__(self):
        return f"Swagger for job {self.job.id}"
