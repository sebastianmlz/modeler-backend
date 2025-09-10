"""
Serializer para el modelo Invite.
"""
from rest_framework import serializers
from ..models import Invite


class InviteSerializer(serializers.ModelSerializer):
    """Serializer para invitaciones."""
    
    class Meta:
        model = Invite
        fields = [
            'id',
            'organization',
            'email',
            'role',
            'token',
            'expires_at',
            'accepted_by',
            'created_at'
        ]
        read_only_fields = ['id', 'token', 'accepted_by', 'created_at']
