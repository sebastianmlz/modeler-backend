"""
ViewSet para el modelo DiagramVersion.
"""
from rest_framework import viewsets, permissions
from ..models import DiagramVersion
from ..serializers import DiagramVersionSerializer


class DiagramVersionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar versiones de diagrama."""
    
    queryset = DiagramVersion.objects.all()
    serializer_class = DiagramVersionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar versiones según el usuario."""
        user = self.request.user
        if user.is_staff:
            return DiagramVersion.objects.all()
        return DiagramVersion.objects.filter(
            diagram__project__organization__membership__user=user,
            diagram__project__organization__membership__status='active'
        ).distinct()
    
    def perform_create(self, serializer):
        """Asignar el usuario actual como creador."""
        serializer.save(created_by=self.request.user)
