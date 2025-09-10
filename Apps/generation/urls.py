"""
URLs para la app generation.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    TemplateViewSet, GenerationJobViewSet, StorageRefViewSet,
    ArtifactViewSet, GenerationLogViewSet, SwaggerSpecViewSet
)

router = DefaultRouter()
router.register(r'templates', TemplateViewSet)
router.register(r'jobs', GenerationJobViewSet)
router.register(r'storage-refs', StorageRefViewSet)
router.register(r'artifacts', ArtifactViewSet)
router.register(r'logs', GenerationLogViewSet)
router.register(r'swagger-specs', SwaggerSpecViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
