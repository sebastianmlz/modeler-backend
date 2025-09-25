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
    # Nuevos endpoints organizacionales (mejor UX/UI)
    path('my-projects/', views.my_projects, name='my_projects'),
    path('projects/<uuid:project_id>/diagrams/', views.project_diagrams, name='project_diagrams'),
    
    # Endpoints de membresía de diagramas 
    path('diagrams/<uuid:diagram_id>/join/', views.join_diagram, name='join_diagram'),
    path('diagrams/<uuid:diagram_id>/members/', views.diagram_members, name='diagram_members'),
    
    # Endpoint legacy (mantener por compatibilidad)
    path('my-diagrams/', views.my_diagrams, name='my_diagrams_legacy'),

    # Endpoints de colaboración existentes
    path('', include(router.urls)),
]
