"""
URLs para autenticación y gestión de usuarios.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.openapi import OpenApiResponse
from .viewsets import UserProfileViewSet, UserRegistrationViewSet

# Extend schema for JWT views with better documentation
TokenObtainPairView = extend_schema_view(
    post=extend_schema(
        operation_id='auth_token_obtain',
        summary='Obtener token JWT',
        description='Autenticar usuario y obtener tokens de acceso y refresh.',
        responses={
            200: OpenApiResponse(description='Tokens obtenidos exitosamente'),
            401: OpenApiResponse(description='Credenciales inválidas'),
        },
        tags=['Authentication']
    )
)(TokenObtainPairView)

TokenRefreshView = extend_schema_view(
    post=extend_schema(
        operation_id='auth_token_refresh',
        summary='Refrescar token JWT',
        description='Obtener nuevo token de acceso usando token de refresh.',
        responses={
            200: OpenApiResponse(description='Token refrescado exitosamente'),
            401: OpenApiResponse(description='Token de refresh inválido o expirado'),
        },
        tags=['Authentication']
    )
)(TokenRefreshView)

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [
    # A01 - Obtener token JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # A02 - Refrescar token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User management endpoints
    path('', include(router.urls)),
]
