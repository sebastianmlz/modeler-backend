"""
ViewSet para el modelo Project según especificación Fase 1.
"""
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from django.db.models import Q
import uuid

from ..models import Project, ProjectMember
from ..serializers import ProjectSerializer
from ..permissions import IsProjectMember


@extend_schema_view(
    list=extend_schema(
        summary="W05 - Listar proyectos de una organización",
        description="Obtener lista de proyectos de una organización específica",
        parameters=[
            OpenApiParameter(
                name='organization',
                description='UUID de la organización para filtrar proyectos',
                required=True,
                type=str
            ),
        ],
        responses={200: ProjectSerializer(many=True)},
        tags=['Workspace']
    ),
    create=extend_schema(
        summary="W04 - Crear proyecto", 
        description="Crear un nuevo proyecto en una organización y asignar al usuario como miembro",
        responses={
            201: ProjectSerializer,
            400: OpenApiResponse(description="Datos inválidos (ej: clave duplicada en organización)"),
            403: OpenApiResponse(description="Sin permisos para crear proyectos en esta organización")
        },
        tags=['Workspace']
    ),
    retrieve=extend_schema(
        summary="W06 - Obtener proyecto por ID",
        description="Obtener detalles de un proyecto específico",
        responses={
            200: ProjectSerializer,
            403: OpenApiResponse(description="Sin permisos para acceder a este proyecto"),
            404: OpenApiResponse(description="Proyecto no encontrado")
        },
        tags=['Workspace']
    )
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar proyectos según Fase 1.
    
    Endpoints implementados:
    - W04: POST /api/projects/ → crear proyecto
    - W05: GET /api/projects/?organization=<uuid> → listar proyectos de una org
    - W06: GET /api/projects/{id}/ → obtener proyecto
    
    Permisos según matriz Fase 1:
    - Crear = miembro de la Organization (owner/admin/editor)
    - Leer = cualquier miembro del proyecto
    """
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'key']
    
    def get_permissions(self):
        """
        Asignar permisos según la acción.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsProjectMember] 
        else:  # list
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filtrar proyectos según el usuario y organización.
        
        W05: Requiere parámetro organization y lista solo proyectos de esa org
        donde el usuario es miembro.
        """
        user = self.request.user
        
        # Obtener parámetro organization
        organization_id = self.request.query_params.get('organization')
        
        # Base queryset: proyectos donde el usuario es miembro de la organización
        if user.is_superuser:
            queryset = Project.objects.all()
        else:
            queryset = Project.objects.filter(
                organization__membership__user=user,
                organization__membership__status='active'
            ).distinct()
        
        # Filtrar por organización si se especifica
        if organization_id:
            try:
                # Validar que es un UUID válido
                uuid.UUID(organization_id)
                queryset = queryset.filter(organization_id=organization_id)
            except (ValueError, TypeError):
                # UUID inválido, devolver queryset vacío
                queryset = queryset.none()
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """
        W05: Listar proyectos requiere parámetro organization.
        """
        organization_id = request.query_params.get('organization')
        
        if not organization_id:
            return Response(
                {
                    "code": "validation_error",
                    "message": "Parámetro 'organization' es requerido",
                    "details": {"organization": "Este parámetro es obligatorio para listar proyectos"}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """
        W04: Crear proyecto y asignar al usuario como miembro.
        """
        # Guardar el proyecto con el usuario como creador
        project = serializer.save(created_by=self.request.user)
        
        # Crear membresía automática como editor
        ProjectMember.objects.create(
            user=self.request.user,
            project=project,
            role='editor'
        )
    
    # Sobrescribir métodos no permitidos en Fase 1
    def update(self, request, *args, **kwargs):
        """PATCH/PUT no están en el alcance de Fase 1."""
        return Response(
            {"detail": "Actualización de proyectos no implementada en Fase 1"}, 
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """PATCH no está en el alcance de Fase 1.""" 
        return Response(
            {"detail": "Actualización parcial de proyectos no implementada en Fase 1"},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    def destroy(self, request, *args, **kwargs):
        """DELETE no está en el alcance de Fase 1."""
        return Response(
            {"detail": "Eliminación de proyectos no implementada en Fase 1"},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
