"""
ViewSet para registro de usuarios.
"""
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.contrib.auth.models import User

from Apps.accounts.serializers import UserRegistrationSerializer, UserWithTokenSerializer


class UserRegistrationViewSet(GenericViewSet):
    """ViewSet para registro de usuarios."""
    
    queryset = User.objects.none()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Registrar nuevo usuario",
        description="Crear una nueva cuenta de usuario con perfil y devolver tokens de acceso",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                response=UserWithTokenSerializer,
                description="Usuario registrado exitosamente con tokens"
            ),
            400: OpenApiResponse(description="Datos de entrada inválidos")
        },
        tags=["Authentication"]
    )
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Registrar un nuevo usuario."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Crear usuario
        user = serializer.save()
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Preparar respuesta con tokens
        user_data = UserWithTokenSerializer(user).data
        user_data['access_token'] = str(access_token)
        user_data['refresh_token'] = str(refresh)
        
        return Response(user_data, status=status.HTTP_201_CREATED)
