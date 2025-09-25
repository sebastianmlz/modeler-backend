from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from Apps.modeling.models import Diagram
from Apps.workspace.models import ProjectMember
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_diagram(request, diagram_id):
    """Unirse a un diagrama (unirse al proyecto del diagrama)."""
    diagram = get_object_or_404(Diagram, id=diagram_id)
    
    # Verificar si ya es miembro
    if ProjectMember.objects.filter(project=diagram.project, user=request.user).exists():
        return Response({'message': 'Already a member'}, status=status.HTTP_200_OK)
    
    # Crear membresía al proyecto con rol viewer por defecto
    ProjectMember.objects.create(
        project=diagram.project,
        user=request.user,
        role='VIEWER'  # Asumiendo que VIEWER existe en ProjectRole
    )
    
    return Response({'message': 'Successfully joined diagram'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def diagram_members(request, diagram_id):
    """Listar miembros del diagrama (miembros del proyecto)."""
    diagram = get_object_or_404(Diagram, id=diagram_id)
    
    # Verificar que el usuario sea miembro del proyecto
    if not ProjectMember.objects.filter(project=diagram.project, user=request.user).exists():
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    
    # Obtener miembros del proyecto
    members = ProjectMember.objects.filter(project=diagram.project).select_related('user')
    data = [
        {
            'id': member.user.id,
            'username': member.user.username,
            'role': member.role,
            'joined_at': member.created_at
        }
        for member in members
    ]
    
    return Response({'members': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_diagrams(request):
    """Listar diagramas donde el usuario es miembro (a través de proyectos)."""
    # Obtener proyectos donde el usuario es miembro
    user_projects = ProjectMember.objects.filter(user=request.user).values_list('project_id', flat=True)
    
    # Obtener diagramas de esos proyectos
    diagrams = Diagram.objects.filter(project_id__in=user_projects).select_related('project')
    
    data = [
        {
            'id': diagram.id,
            'name': diagram.name,
            'project': diagram.project.name,
            'created_at': diagram.created_at
        }
        for diagram in diagrams
    ]
    
    return Response({'diagrams': data})