"""
Serializer para el modelo ProjectMember.
"""
from rest_framework import serializers
from ..models import ProjectMember


class ProjectMemberSerializer(serializers.ModelSerializer):
    """Serializer para miembros de proyecto."""
    
    class Meta:
        model = ProjectMember
        fields = [
            'id',
            'project',
            'user',
            'role',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
