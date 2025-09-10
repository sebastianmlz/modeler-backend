"""
Serializer para el modelo UserProfile.
"""
from rest_framework import serializers
from ..models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de usuario."""
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'display_name',
            'avatar_url',
            'locale',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_display_name(self, value):
        """Validar que el nombre para mostrar no esté vacío."""
        if not value.strip():
            raise serializers.ValidationError("El nombre para mostrar no puede estar vacío.")
        return value.strip()
