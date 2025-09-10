"""
ViewSet para el modelo Presence.
"""
from rest_framework import viewsets, permissions
from ..models import Presence
from ..serializers import PresenceSerializer


class PresenceViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar presencia de usuarios."""
    
    queryset = Presence.objects.all()
    serializer_class = PresenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar presencias por sesiones accesibles al usuario."""
        user = self.request.user
        if user.is_superuser:
            return Presence.objects.all()
        
        # Filtrar por sesiones de diagramas accesibles
        return Presence.objects.filter(
            session__diagram__project__organization__membership__user=user,
            session__diagram__project__organization__membership__status='active'
        )
