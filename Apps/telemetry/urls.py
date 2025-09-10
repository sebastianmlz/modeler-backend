"""
URLs para la app telemetry.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import EventViewSet, AuditLogViewSet, UsageStatViewSet, ErrorLogViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'usage-stats', UsageStatViewSet)
router.register(r'error-logs', ErrorLogViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
