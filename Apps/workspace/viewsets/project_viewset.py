"""
ViewSet para el modelo Project.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Project
from ..serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar proyectos."""
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar proyectos según el usuario y organización."""
        user = self.request.user
        if user.is_staff:
            return Project.objects.all()
        
        # Filtrar proyectos de organizaciones donde el usuario es miembro
        return Project.objects.filter(
            organization__membership__user=user,
            organization__membership__status='active'
        ).distinct()
    
    def perform_create(self, serializer):
        """Asignar el usuario actual como creador."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Obtener miembros del proyecto."""
        project = self.get_object()
        members = project.projectmember_set.all()
        return Response({
            'project': project.name,
            'members_count': members.count()
        })
