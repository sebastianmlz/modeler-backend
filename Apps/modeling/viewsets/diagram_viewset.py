"""
ViewSet para el modelo Diagram según especificación Fase 1.
"""
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from django.utils import timezone
import uuid

from ..models import Diagram
from ..serializers import DiagramSerializer, DiagramUpdateSerializer
from ..permissions import IsProjectMemberForDiagram, CanEditDiagram


@extend_schema_view(
    list=extend_schema(
        summary="M02 - Listar diagramas del proyecto",
        description="Obtener lista de diagramas de un proyecto específico",
        parameters=[
            OpenApiParameter(
                name='project',
                description='UUID del proyecto para filtrar diagramas',
                required=True,
                type=str
            ),
        ],
        responses={200: DiagramSerializer(many=True)},
        tags=['Modeling']
    ),
    create=extend_schema(
        summary="M01 - Crear diagrama", 
        description="Crear un nuevo diagrama en un proyecto",
        responses={
            201: DiagramSerializer,
            400: OpenApiResponse(description="Datos inválidos (ej: nombre duplicado en proyecto)"),
            403: OpenApiResponse(description="Sin permisos para crear diagramas en este proyecto")
        },
        tags=['Modeling']
    ),
    retrieve=extend_schema(
        summary="M03 - Obtener diagrama por ID",
        description="Obtener detalles de un diagrama específico",
        responses={
            200: DiagramSerializer,
            403: OpenApiResponse(description="Sin permisos para acceder a este diagrama"),
            404: OpenApiResponse(description="Diagrama no encontrado")
        },
        tags=['Modeling']
    ),
    partial_update=extend_schema(
        summary="M03 - Renombrar diagrama",
        description="Actualizar el nombre de un diagrama",
        request=DiagramUpdateSerializer,
        responses={
            200: DiagramSerializer,
            400: OpenApiResponse(description="Datos inválidos (ej: nombre duplicado)"),
            403: OpenApiResponse(description="Sin permisos para editar este diagrama")
        },
        tags=['Modeling']
    ),
    destroy=extend_schema(
        summary="M03 - Eliminar diagrama (soft delete)",
        description="Marcar un diagrama como eliminado (soft delete)",
        responses={
            204: OpenApiResponse(description="Diagrama eliminado exitosamente"),
            403: OpenApiResponse(description="Sin permisos para eliminar este diagrama"),
            404: OpenApiResponse(description="Diagrama no encontrado")
        },
        tags=['Modeling']
    )
)
class DiagramViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar diagramas según Fase 1.
    
    Endpoints implementados:
    - M01: POST /api/diagrams/ → crear diagrama
    - M02: GET /api/diagrams/?project=<uuid> → listar diagramas del proyecto
    - M03: GET /api/diagrams/{id}/ → obtener diagrama
    - M03: PATCH /api/diagrams/{id}/ → renombrar diagrama
    - M03: DELETE /api/diagrams/{id}/ → eliminar diagrama (soft delete)
    
    Permisos según matriz Fase 1:
    - Crear/editar/eliminar = miembro del proyecto (editor+)
    - Leer = cualquier miembro del proyecto
    """
    
    queryset = Diagram.objects.filter(deleted_at__isnull=True)  # Excluir soft deleted
    serializer_class = DiagramSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_permissions(self):
        """
        Asignar permisos según la acción.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsProjectMemberForDiagram] 
        elif self.action in ['partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, CanEditDiagram]
        else:  # list
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Usar serializer específico para updates.
        """
        if self.action == 'partial_update':
            return DiagramUpdateSerializer
        return DiagramSerializer
    
    def get_queryset(self):
        """
        Filtrar diagramas según el usuario y proyecto.
        
        M02: Requiere parámetro project y lista solo diagramas de ese proyecto
        donde el usuario es miembro.
        """
        user = self.request.user
        
        # Obtener parámetro project
        project_id = self.request.query_params.get('project')
        
        # Base queryset: diagramas donde el usuario es miembro del proyecto
        if user.is_superuser:
            queryset = Diagram.objects.filter(deleted_at__isnull=True)
        else:
            queryset = Diagram.objects.filter(
                project__organization__membership__user=user,
                project__organization__membership__status='active',
                deleted_at__isnull=True
            ).distinct()
        
        # Filtrar por proyecto si se especifica
        if project_id:
            try:
                # Validar que es un UUID válido
                uuid.UUID(project_id)
                queryset = queryset.filter(project_id=project_id)
            except (ValueError, TypeError):
                # UUID inválido, devolver queryset vacío
                queryset = queryset.none()
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        M02: Listar diagramas requiere parámetro project.
        """
        project_id = request.query_params.get('project')
        
        if not project_id:
            return Response(
                {
                    "code": "validation_error",
                    "message": "Parámetro 'project' es requerido",
                    "details": {"project": "Este parámetro es obligatorio para listar diagramas"}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """
        M01: Crear diagrama.
        """
        # Guardar el diagrama con el usuario como creador
        serializer.save(created_by=self.request.user)
    
    def perform_destroy(self, instance):
        """
        M03: Soft delete del diagrama.
        """
        # Marcar como eliminado en lugar de eliminar físicamente
        instance.deleted_at = timezone.now()
        instance.save()
    
    # Sobrescribir método no permitido en Fase 1
    def update(self, request, *args, **kwargs):
        """PUT completo no está en el alcance de Fase 1."""
        return Response(
            {"detail": "Actualización completa de diagramas no implementada en Fase 1. Use PATCH para renombrar."}, 
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
