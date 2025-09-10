"""
ViewSet para el modelo EnumValue.
"""
from rest_framework import viewsets, permissions
from ..models import EnumValue
from ..serializers import EnumValueSerializer


class EnumValueViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar valores de enumeración."""
    
    queryset = EnumValue.objects.all()
    serializer_class = EnumValueSerializer
    permission_classes = [permissions.IsAuthenticated]
