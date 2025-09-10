"""
ViewSet para el modelo ModelClass.
"""
from rest_framework import viewsets, permissions
from ..models import ModelClass
from ..serializers import ModelClassSerializer


class ModelClassViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar clases UML."""
    
    queryset = ModelClass.objects.all()
    serializer_class = ModelClassSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar clases según el diagrama y usuario."""
        user = self.request.user
        if user.is_staff:
            return ModelClass.objects.all()
        return ModelClass.objects.filter(
            diagram__project__organization__membership__user=user,
            diagram__project__organization__membership__status='active'
        ).distinct()
