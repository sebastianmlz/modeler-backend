"""
ViewSet para versiones de diagramas - M04, M05, M06.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from Apps.modeling.models import DiagramVersion, Diagram
from Apps.modeling.serializers import (
    DiagramVersionSerializer, 
    DiagramVersionDetailSerializer, 
    DiagramVersionListSerializer
)
from Apps.modeling.permissions import (
    CanCreateDiagramVersion, 
    CanViewDiagramVersion, 
    CanListDiagramVersions
)


class DiagramVersionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar versiones de diagramas.
    
    Implementa endpoints:
    - M04: POST /api/diagram-versions/ - Crear versión del diagrama
    - M05: GET /api/diagram-versions/?diagram={id} - Listar versiones de un diagrama
    - M06: GET /api/diagram-versions/{id}/ - Obtener versión específica
    """
    
    queryset = DiagramVersion.objects.select_related(
        'diagram', 'diagram__project', 'diagram__project__organization', 'created_by'
    ).all()
    
    serializer_class = DiagramVersionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['diagram']
    ordering_fields = ['version_number', 'created_at']
    ordering = ['-version_number']
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción."""
        if self.action == 'list':
            return DiagramVersionListSerializer
        elif self.action == 'retrieve':
            return DiagramVersionDetailSerializer
        return DiagramVersionSerializer
    
    def get_permissions(self):
        """Asigna permisos específicos según la acción."""
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanCreateDiagramVersion]
        elif self.action == 'list':
            permission_classes = [permissions.IsAuthenticated, CanListDiagramVersions]
        elif self.action in ['retrieve']:
            permission_classes = [permissions.IsAuthenticated, CanViewDiagramVersion]
        else:
            # Bloquear otras acciones (update, destroy, etc.)
            permission_classes = [permissions.IsAdminUser]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filtra versiones según los permisos del usuario."""
        user = self.request.user
        
        if user.is_superuser:
            return self.queryset
        
        # Solo versiones de diagramas en proyectos donde el usuario es miembro
        return self.queryset.filter(
            diagram__project__organization__membership__user=user,
            diagram__project__organization__membership__status='active'
        ).distinct()
    
    @extend_schema(
        operation_id='create_diagram_version',
        summary='M04 - Crear versión del diagrama',
        description='''
        Crea una nueva versión (snapshot) del diagrama especificado.
        
        **Validaciones:**
        - El usuario debe ser miembro del proyecto
        - El diagrama debe existir y no estar eliminado
        - El snapshot debe tener la estructura JSON válida
        - El número de versión se asigna automáticamente (secuencial)
        
        **Estructura del snapshot:**
        ```json
        {
            "classes": [],
            "relations": [],
            "metadata": {}
        }
        ```
        ''',
        request=DiagramVersionSerializer,
        responses={
            201: DiagramVersionSerializer,
            400: 'Error de validación',
            403: 'Sin permisos',
            404: 'Diagrama no encontrado'
        }
    )
    def create(self, request, *args, **kwargs):
        """M04 - Crear versión del diagrama."""
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        operation_id='list_diagram_versions',
        summary='M05 - Listar versiones de un diagrama',
        description='''
        Lista todas las versiones del diagrama especificado.
        
        **Parámetros requeridos:**
        - `diagram`: ID del diagrama (UUID)
        
        **Filtros disponibles:**
        - Ordenamiento por version_number o created_at
        - Paginación automática
        
        **Nota:** El snapshot completo no se incluye en el listado por rendimiento.
        Use M06 para obtener el snapshot de una versión específica.
        ''',
        parameters=[
            OpenApiParameter(
                name='diagram',
                description='ID del diagrama',
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='ordering',
                description='Campo de ordenamiento: version_number, -version_number, created_at, -created_at',
                required=False,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY
            )
        ],
        responses={
            200: DiagramVersionListSerializer(many=True),
            400: 'Parámetro diagram requerido',
            403: 'Sin permisos',
            404: 'Diagrama no encontrado'
        }
    )
    def list(self, request, *args, **kwargs):
        """M05 - Listar versiones de un diagrama."""
        diagram_id = request.query_params.get('diagram')
        
        if not diagram_id:
            return Response(
                {'error': 'El parámetro "diagram" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el diagrama existe y el usuario tiene permisos
        try:
            diagram = Diagram.objects.get(id=diagram_id)
            
            # Verificar permisos de lectura
            if not diagram.project.organization.membership_set.filter(
                user=request.user, status='active'
            ).exists() and not request.user.is_superuser:
                return Response(
                    {'error': 'Sin permisos para acceder a este diagrama'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
        except Diagram.DoesNotExist:
            return Response(
                {'error': 'Diagrama no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        operation_id='retrieve_diagram_version',
        summary='M06 - Obtener versión específica del diagrama',
        description='''
        Obtiene los detalles completos de una versión específica del diagrama,
        incluyendo el snapshot JSON completo.
        
        **Incluye:**
        - Datos de la versión (número, mensaje, fecha)
        - Información del creador
        - Información del diagrama y proyecto
        - Snapshot JSON completo del diagrama
        
        **Casos de uso:**
        - Revisar el estado del diagrama en un momento específico
        - Restaurar/comparar versiones
        - Auditoría de cambios
        ''',
        responses={
            200: DiagramVersionDetailSerializer,
            403: 'Sin permisos',
            404: 'Versión no encontrada'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """M06 - Obtener versión específica del diagrama."""
        return super().retrieve(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Asigna el usuario actual como creador de la versión."""
        serializer.save(created_by=self.request.user)
    
    # Bloquear acciones no permitidas en Fase 1
    def update(self, request, *args, **kwargs):
        """Las versiones no se pueden modificar."""
        return Response(
            {'error': 'No se pueden modificar las versiones de diagramas'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Las versiones no se pueden modificar."""
        return Response(
            {'error': 'No se pueden modificar las versiones de diagramas'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """Las versiones no se pueden eliminar en Fase 1."""
        return Response(
            {'error': 'No se pueden eliminar las versiones de diagramas en Fase 1'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
