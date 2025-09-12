"""
ViewSet para bloqueos de diagramas - C01, C02, C03, C04.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.utils import timezone
from Apps.collaboration.models import Lock
from Apps.modeling.models import Diagram
from Apps.collaboration.serializers import (
    LockSerializer, 
    LockDetailSerializer, 
    LockExtendSerializer
)
from Apps.collaboration.permissions import (
    CanCreateLock, 
    CanViewLock, 
    CanReleaseLock, 
    CanListLocks,
    CanExtendLock
)


class LockViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar bloqueos de diagramas.
    
    Implementa endpoints:
    - C01: POST /api/locks/ - Crear bloqueo en diagrama
    - C02: GET /api/locks/?project={id} - Listar bloqueos del proyecto
    - C03: GET /api/locks/{id}/ - Obtener detalles del bloqueo
    - C04: DELETE /api/locks/{id}/ - Liberar bloqueo
    """
    
    queryset = Lock.objects.select_related(
        'diagram', 'diagram__project', 'diagram__project__organization', 'locked_by'
    ).all()
    
    serializer_class = LockSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['diagram', 'locked_by', 'purpose']
    ordering_fields = ['locked_at', 'expires_at']
    ordering = ['-locked_at']
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción."""
        if self.action == 'retrieve':
            return LockDetailSerializer
        elif self.action == 'extend_lock':
            return LockExtendSerializer
        return LockSerializer
    
    def get_permissions(self):
        """Asigna permisos específicos según la acción."""
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanCreateLock]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated, CanListLocks]
        elif self.action in ['retrieve']:
            permission_classes = [permissions.IsAuthenticated, CanViewLock]
        elif self.action in ['destroy']:
            permission_classes = [permissions.IsAuthenticated, CanReleaseLock]
        elif self.action == 'extend_lock':
            permission_classes = [permissions.IsAuthenticated, CanExtendLock]
        else:
            # Bloquear otras acciones (update, partial_update)
            permission_classes = [permissions.IsAdminUser]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filtra bloqueos según los permisos del usuario y limpia expirados."""
        # Limpiar bloqueos expirados automáticamente
        Lock.cleanup_expired_locks()
        
        user = self.request.user
        
        if user.is_superuser:
            return self.queryset
        
        # Solo bloqueos de diagramas en proyectos donde el usuario es miembro
        return self.queryset.filter(
            diagram__project__organization__membership__user=user,
            diagram__project__organization__membership__status='active'
        ).distinct()
    
    @extend_schema(
        operation_id='create_lock',
        summary='C01 - Crear bloqueo en diagrama',
        description='''
        Crea un nuevo bloqueo en el diagrama especificado para edición exclusiva.
        
        **Características del bloqueo:**
        - TTL por defecto: 30 minutos
        - Solo un bloqueo activo por diagrama
        - El creador puede extender o liberar el bloqueo
        - Los admins pueden liberar cualquier bloqueo
        
        **Validaciones:**
        - El usuario debe ser miembro del proyecto
        - El diagrama debe existir y no estar eliminado
        - No debe existir un bloqueo activo en el diagrama
        
        **Propósitos válidos:**
        - editing: Edición del diagrama (por defecto)
        - reviewing: Revisión del diagrama
        - testing: Pruebas del diagrama
        - maintenance: Mantenimiento del diagrama
        ''',
        request=LockSerializer,
        responses={
            201: LockSerializer,
            400: 'Error de validación o diagrama ya bloqueado',
            403: 'Sin permisos',
            404: 'Diagrama no encontrado'
        }
    )
    def create(self, request, *args, **kwargs):
        """C01 - Crear bloqueo en diagrama."""
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        operation_id='list_locks',
        summary='C02 - Listar bloqueos del proyecto',
        description='''
        Lista todos los bloqueos activos del proyecto especificado.
        
        **Filtros disponibles:**
        - `project`: ID del proyecto (requerido)
        - `diagram`: ID del diagrama específico
        - `locked_by`: ID del usuario que creó el bloqueo
        - `purpose`: Propósito del bloqueo
        
        **Nota:** Solo se muestran bloqueos no expirados. 
        Los bloqueos expirados se limpian automáticamente.
        ''',
        parameters=[
            OpenApiParameter(
                name='project',
                description='ID del proyecto',
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='diagram',
                description='ID del diagrama específico',
                required=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='locked_by',
                description='ID del usuario que creó el bloqueo',
                required=False,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='purpose',
                description='Propósito del bloqueo',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            )
        ],
        responses={
            200: LockSerializer(many=True),
            400: 'Parámetro project requerido',
            403: 'Sin permisos'
        }
    )
    def list(self, request, *args, **kwargs):
        """C02 - Listar bloqueos del proyecto."""
        project_id = request.query_params.get('project')
        
        if not project_id:
            return Response(
                {'error': 'El parámetro "project" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtrar por proyecto en el queryset
        queryset = self.get_queryset().filter(diagram__project_id=project_id)
        
        # Aplicar filtros adicionales
        filtered_queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        operation_id='retrieve_lock',
        summary='C03 - Obtener detalles del bloqueo',
        description='''
        Obtiene los detalles completos de un bloqueo específico.
        
        **Incluye:**
        - Información del bloqueo (fechas, propósito, tiempo restante)
        - Datos del propietario del bloqueo
        - Información del diagrama y proyecto
        - Estado de expiración
        - Duración total y tiempo restante
        
        **Casos de uso:**
        - Verificar quién tiene bloqueado un diagrama
        - Consultar tiempo restante del bloqueo
        - Auditoría de bloqueos del proyecto
        ''',
        responses={
            200: LockDetailSerializer,
            403: 'Sin permisos',
            404: 'Bloqueo no encontrado'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """C03 - Obtener detalles del bloqueo."""
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        operation_id='release_lock',
        summary='C04 - Liberar bloqueo',
        description='''
        Libera (elimina) un bloqueo específico del diagrama.
        
        **Permisos requeridos:**
        - El propietario del bloqueo puede liberarlo siempre
        - Los admins/owners de la organización pueden liberar cualquier bloqueo
        - Los superusers pueden liberar cualquier bloqueo
        
        **Efecto:**
        - El diagrama queda disponible para ser bloqueado por otros usuarios
        - El bloqueo se elimina permanentemente
        - No es posible recuperar un bloqueo liberado
        
        **Casos de uso:**
        - Finalizar sesión de edición
        - Liberar bloqueos abandonados (por admins)
        - Resolver conflictos de bloqueos
        ''',
        responses={
            204: 'Bloqueo liberado exitosamente',
            403: 'Sin permisos para liberar este bloqueo',
            404: 'Bloqueo no encontrado'
        }
    )
    def destroy(self, request, *args, **kwargs):
        """C04 - Liberar bloqueo."""
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        operation_id='extend_lock',
        summary='Extender duración del bloqueo',
        description='''
        Extiende la duración de un bloqueo existente.
        
        **Restricciones:**
        - Solo el propietario del bloqueo puede extenderlo
        - Máximo 120 minutos por extensión
        - El bloqueo debe estar activo (no expirado)
        
        **Casos de uso:**
        - Continuar trabajando en un diagrama
        - Evitar perder el bloqueo durante trabajo prolongado
        ''',
        request=LockExtendSerializer,
        responses={
            200: LockDetailSerializer,
            400: 'Error de validación',
            403: 'Sin permisos',
            404: 'Bloqueo no encontrado'
        }
    )
    @action(detail=True, methods=['post'])
    def extend_lock(self, request, pk=None):
        """Extender duración del bloqueo."""
        lock = self.get_object()
        
        # Verificar que el bloqueo no haya expirado
        if lock.is_expired:
            return Response(
                {'error': 'No se puede extender un bloqueo expirado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            minutes = serializer.validated_data['minutes']
            lock.extend_lock(minutes)
            
            detail_serializer = LockDetailSerializer(lock, context={'request': request})
            return Response(detail_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        """Asigna el usuario actual como propietario del bloqueo."""
        serializer.save(locked_by=self.request.user)
    
    # Bloquear acciones no permitidas en Fase 1
    def update(self, request, *args, **kwargs):
        """Los bloqueos no se pueden modificar."""
        return Response(
            {'error': 'No se pueden modificar los bloqueos'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Los bloqueos no se pueden modificar."""
        return Response(
            {'error': 'No se pueden modificar los bloqueos'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )