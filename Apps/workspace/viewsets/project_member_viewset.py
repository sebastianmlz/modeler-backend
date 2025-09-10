"""
ViewSet para el modelo ProjectMember.
"""
from rest_framework import viewsets, permissions
from ..models import ProjectMember
from ..serializers import ProjectMemberSerializer


class ProjectMemberViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar miembros de proyecto."""
    
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar miembros según el usuario."""
        user = self.request.user
        if user.is_staff:
            return ProjectMember.objects.all()
        # Mostrar miembros de proyectos donde el usuario tiene acceso
        return ProjectMember.objects.filter(
            project__organization__membership__user=user,
            project__organization__membership__status='active'
        )
