"""
ViewSet para el modelo ModelMethod.
"""
from rest_framework import viewsets, permissions
from ..models import ModelMethod
from ..serializers import ModelMethodSerializer


class ModelMethodViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar métodos de clase."""
    
    queryset = ModelMethod.objects.all()
    serializer_class = ModelMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
