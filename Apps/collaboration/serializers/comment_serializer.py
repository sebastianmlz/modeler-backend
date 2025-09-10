"""
Serializer para Comment.
"""
from rest_framework import serializers
from ..models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Comment."""
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'deleted_at']
