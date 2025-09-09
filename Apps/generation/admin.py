from django.contrib import admin
from .models import Template, GenerationJob, StorageRef, Artifact, GenerationLog, SwaggerSpec

# Registrar modelos relacionados con generación de código
admin.site.register(Template)
admin.site.register(GenerationJob)
admin.site.register(StorageRef)
admin.site.register(Artifact)
admin.site.register(GenerationLog)
admin.site.register(SwaggerSpec)
