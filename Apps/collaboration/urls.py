"""
URLs para la app collaboration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CollabSessionViewSet, PresenceViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'sessions', CollabSessionViewSet)
router.register(r'presence', PresenceViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
