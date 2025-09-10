"""
URLs para la app workspace.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    OrganizationViewSet,
    MembershipViewSet,
    InviteViewSet,
    ProjectViewSet,
    ProjectMemberViewSet
)

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'invites', InviteViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-members', ProjectMemberViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
