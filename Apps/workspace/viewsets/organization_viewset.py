"""
ViewSet para el modelo Organization según especificación Fase 1.
"""
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse

from ..models import Organization, Membership
from ..serializers import OrganizationSerializer
from ..permissions import IsOrganizationMember


@extend_schema_view(
    list=extend_schema(
        summary="W02 - Listar mis organizaciones",
        description="Obtener lista de organizaciones donde el usuario es miembro",
        parameters=[
            OpenApiParameter(
                name='search',
                description='Buscar organizaciones por nombre',
                required=False,
                type=str
            ),
        ],
        responses={200: OrganizationSerializer(many=True)},
        tags=['Workspace']
    ),
    create=extend_schema(
        summary="W01 - Crear organización", 
        description="Crear una nueva organización y asignar al usuario como owner",
        responses={
            201: OrganizationSerializer,
            400: OpenApiResponse(description="Datos inválidos (ej: slug duplicado)")
        },
        tags=['Workspace']
    ),
    retrieve=extend_schema(
        summary="W03 - Obtener organización por ID",
        description="Obtener detalles de una organización específica",
        responses={
            200: OrganizationSerializer,
            403: OpenApiResponse(description="Sin permisos para acceder a esta organización"),
            404: OpenApiResponse(description="Organización no encontrada")
        },
        tags=['Workspace']
    )
)
class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar organizaciones según Fase 1.
    
    Endpoints implementados:
    - W01: POST /api/organizations/ → crear organización
    - W02: GET /api/organizations/ → listar mis organizaciones  
    - W03: GET /api/organizations/{id}/ → obtener organización
    
    Permisos según matriz Fase 1:
    - Crear = IsAuthenticated
    - Listar/Obtener = miembro de la organización
    """
    
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_permissions(self):
        """
        Asignar permisos según la acción.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsOrganizationMember] 
        else:  # list
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filtrar organizaciones según el usuario.
        
        W02: Lista solo organizaciones donde el usuario es miembro.
        """
        user = self.request.user
        
        # Superusers ven todas las organizaciones
        if user.is_superuser:
            return Organization.objects.all()
        
        # Usuarios normales: solo organizaciones donde son miembros
        return Organization.objects.filter(
            membership__user=user,
            membership__status='active'
        ).distinct()
    
    def perform_create(self, serializer):
        """
        W01: Crear organización y asignar al usuario como owner.
        """
        # Guardar la organización con el usuario como creador
        organization = serializer.save(created_by=self.request.user)
        
        # Crear membresía automática como owner
        Membership.objects.create(
            user=self.request.user,
            organization=organization,
            role='owner',
            status='active'
        )
    
    # Sobrescribir métodos no permitidos en Fase 1
    def update(self, request, *args, **kwargs):
        """PATCH/PUT no están en el alcance de Fase 1."""
        return Response(
            {"detail": "Actualización de organizaciones no implementada en Fase 1"}, 
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """PATCH no está en el alcance de Fase 1.""" 
        return Response(
            {"detail": "Actualización parcial de organizaciones no implementada en Fase 1"},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
    
    def destroy(self, request, *args, **kwargs):
        """DELETE no está en el alcance de Fase 1."""
        return Response(
            {"detail": "Eliminación de organizaciones no implementada en Fase 1"},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
