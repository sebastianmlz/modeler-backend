"""
ViewSet para el modelo Comment.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Comment
from ..serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar comentarios."""
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar comentarios por proyectos accesibles al usuario."""
        user = self.request.user
        if user.is_superuser:
            return Comment.objects.all()
        
        # Filtrar por proyectos donde el usuario tiene acceso
        return Comment.objects.filter(
            project__organization__membership__user=user,
            project__organization__membership__status='active'
        )
    
    def perform_create(self, serializer):
        """Establecer el autor del comentario al usuario actual."""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Obtener respuestas a un comentario."""
        comment = self.get_object()
        replies = Comment.objects.filter(parent=comment)
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)
