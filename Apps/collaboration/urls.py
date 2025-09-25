"""
URLs para la app collaboration.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .viewsets import (
    collab_session_viewset,
    comment_viewset,
    lock_viewset,
    presence_viewset
)

router = DefaultRouter()
router.register(r'sessions', collab_session_viewset.CollabSessionViewSet)
router.register(r'comments', comment_viewset.CommentViewSet)
router.register(r'locks', lock_viewset.LockViewSet)
router.register(r'presence', presence_viewset.PresenceViewSet)

urlpatterns = [
    # Endpoints de membresía de diagramas (primero)
    path('my-diagrams/', views.my_diagrams, name='my_diagrams'),
    path('diagrams/<uuid:diagram_id>/join/', views.join_diagram, name='join_diagram'),
    path('diagrams/<uuid:diagram_id>/members/', views.diagram_members, name='diagram_members'),

    # Endpoints de colaboración existentes
    path('', include(router.urls)),
]
