"""
ViewSet para el modelo ModelRelation.
"""
from rest_framework import viewsets, permissions
from ..models import ModelRelation
from ..serializers import ModelRelationSerializer


class ModelRelationViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar relaciones entre clases."""
    
    queryset = ModelRelation.objects.all()
    serializer_class = ModelRelationSerializer
    permission_classes = [permissions.IsAuthenticated]
