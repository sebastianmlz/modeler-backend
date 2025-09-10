"""
Serializer para el modelo Membership.
"""
from rest_framework import serializers
from ..models import Membership


class MembershipSerializer(serializers.ModelSerializer):
    """Serializer para membresías."""
    
    class Meta:
        model = Membership
        fields = [
            'id',
            'organization',
            'user',
            'role',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
