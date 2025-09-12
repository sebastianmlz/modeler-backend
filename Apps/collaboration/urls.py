"""
URLs para la app collaboration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CollabSessionViewSet, PresenceViewSet, CommentViewSet, LockViewSet

router = DefaultRouter()
router.register(r'sessions', CollabSessionViewSet)
router.register(r'presence', PresenceViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'locks', LockViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
