"""
ViewSet para el modelo Organization.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Organization
from ..serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar organizaciones."""
    
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar organizaciones según el usuario."""
        user = self.request.user
        if user.is_staff:
            return Organization.objects.all()
        # Filtrar solo las organizaciones donde el usuario es miembro
        return Organization.objects.filter(
            membership__user=user,
            membership__status='active'
        ).distinct()
    
    def perform_create(self, serializer):
        """Asignar el usuario actual como creador."""
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Obtener miembros de la organización."""
        organization = self.get_object()
        members = organization.membership_set.filter(status='active')
        # Aquí podrías usar un serializer específico para los miembros
        return Response({
            'organization': organization.name,
            'members_count': members.count()
        })
