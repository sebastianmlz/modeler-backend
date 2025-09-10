"""
ViewSet para el modelo Diagram.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Diagram
from ..serializers import DiagramSerializer


class DiagramViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar diagramas."""
    
    queryset = Diagram.objects.all()
    serializer_class = DiagramSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar diagramas según el proyecto y usuario."""
        user = self.request.user
        if user.is_staff:
            return Diagram.objects.all()
        # Filtrar por proyectos donde el usuario tiene acceso
        return Diagram.objects.filter(
            project__organization__membership__user=user,
            project__organization__membership__status='active'
        ).distinct()
    
    def perform_create(self, serializer):
        """Asignar el usuario actual como creador."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def classes(self, request, pk=None):
        """Obtener clases del diagrama."""
        diagram = self.get_object()
        classes = diagram.modelclass_set.all()
        return Response({
            'diagram': diagram.name,
            'classes_count': classes.count()
        })
