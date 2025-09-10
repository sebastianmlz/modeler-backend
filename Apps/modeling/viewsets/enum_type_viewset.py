"""
ViewSet para el modelo EnumType.
"""
from rest_framework import viewsets, permissions
from ..models import EnumType
from ..serializers import EnumTypeSerializer


class EnumTypeViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar tipos enumerados."""
    
    queryset = EnumType.objects.all()
    serializer_class = EnumTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
