"""
ViewSet para el modelo CollabSession.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import CollabSession
from ..serializers import CollabSessionSerializer


class CollabSessionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar sesiones colaborativas."""
    
    queryset = CollabSession.objects.all()
    serializer_class = CollabSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar sesiones por proyecto del usuario."""
        user = self.request.user
        if user.is_superuser:
            return CollabSession.objects.all()
        
        # Filtrar por diagramas de proyectos donde el usuario tiene acceso
        return CollabSession.objects.filter(
            diagram__project__organization__membership__user=user,
            diagram__project__organization__membership__status='active'
        )
    
    @action(detail=True, methods=['post'])
    def end_session(self, request, pk=None):
        """Finalizar una sesión colaborativa."""
        session = self.get_object()
        session.ended_at = timezone.now()
        session.save()
        return Response({'status': 'session ended'})
