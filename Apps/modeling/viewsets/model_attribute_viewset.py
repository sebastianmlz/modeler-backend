"""
ViewSet para el modelo ModelAttribute.
"""
from rest_framework import viewsets, permissions
from ..models import ModelAttribute
from ..serializers import ModelAttributeSerializer


class ModelAttributeViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar atributos de clase."""
    
    queryset = ModelAttribute.objects.all()
    serializer_class = ModelAttributeSerializer
    permission_classes = [permissions.IsAuthenticated]
