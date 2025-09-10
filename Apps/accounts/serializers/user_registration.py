"""
Serializer para registro de usuarios.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from Apps.accounts.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios."""
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        help_text="Contraseña del usuario"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Confirmación de contraseña"
    )
    display_name = serializers.CharField(
        max_length=120,
        help_text="Nombre para mostrar en la interfaz"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm', 'display_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden.'
            })
        return attrs
    
    def create(self, validated_data):
        """Crear usuario y su perfil."""
        # Remover campos que no pertenecen al modelo User
        display_name = validated_data.pop('display_name')
        validated_data.pop('password_confirm')
        
        # Crear usuario
        user = User.objects.create_user(**validated_data)
        
        # Crear perfil
        UserProfile.objects.create(
            user=user,
            display_name=display_name,
            locale='en-US'
        )
        
        return user


class UserWithTokenSerializer(serializers.ModelSerializer):
    """Serializer para usuario con token y perfil."""
    
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'access_token', 'refresh_token', 'profile']
    
    def get_profile(self, obj):
        """Obtener datos del perfil del usuario."""
        try:
            profile = obj.userprofile
            return {
                'id': str(profile.id),
                'display_name': profile.display_name,
                'avatar_url': profile.avatar_url,
                'locale': profile.locale
            }
        except UserProfile.DoesNotExist:
            return None
