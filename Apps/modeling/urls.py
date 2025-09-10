"""
URLs para la app modeling.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    DiagramViewSet,
    DiagramVersionViewSet,
    ModelClassViewSet,
    ModelAttributeViewSet,
    ModelMethodViewSet,
    EnumTypeViewSet,
    EnumValueViewSet,
    ModelRelationViewSet
)

router = DefaultRouter()
router.register(r'diagrams', DiagramViewSet)
router.register(r'diagram-versions', DiagramVersionViewSet)
router.register(r'model-classes', ModelClassViewSet)
router.register(r'model-attributes', ModelAttributeViewSet)
router.register(r'model-methods', ModelMethodViewSet)
router.register(r'enum-types', EnumTypeViewSet)
router.register(r'enum-values', EnumValueViewSet)
router.register(r'model-relations', ModelRelationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
