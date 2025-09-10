"""
ViewSet para el modelo Invite.
"""
from rest_framework import viewsets, permissions
from ..models import Invite
from ..serializers import InviteSerializer


class InviteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar invitaciones."""
    
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar invitaciones según el usuario."""
        user = self.request.user
        if user.is_staff:
            return Invite.objects.all()
        # Mostrar invitaciones de organizaciones donde el usuario tiene permisos
        return Invite.objects.filter(
            organization__membership__user=user,
            organization__membership__role__in=['owner', 'admin']
        )
