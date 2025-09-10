"""
ViewSet para el modelo Membership.
"""
from rest_framework import viewsets, permissions
from ..models import Membership
from ..serializers import MembershipSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar membresías."""
    
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar membresías según el usuario."""
        user = self.request.user
        if user.is_staff:
            return Membership.objects.all()
        return Membership.objects.filter(user=user)
