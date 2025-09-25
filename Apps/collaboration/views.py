from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from Apps.modeling.models import Diagram
from Apps.workspace.models import ProjectMember, Project
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_projects(request):
    """Listar proyectos donde el usuario es miembro con sus diagramas."""
    # Obtener proyectos donde el usuario es miembro
    project_memberships = ProjectMember.objects.filter(
        user=request.user
    ).select_related('project', 'project__organization')
    
    projects_data = []
    for membership in project_memberships:
        project = membership.project
        
        # Obtener diagramas del proyecto
        diagrams = Diagram.objects.filter(project=project).order_by('name')
        diagrams_data = [
            {
                'id': diagram.id,
                'name': diagram.name,
                'current_version': diagram.current_version,
                'created_by': diagram.created_by.username,
                'created_at': diagram.created_at
            }
            for diagram in diagrams
        ]
        
        projects_data.append({
            'project': {
                'id': project.id,
                'name': project.name,
                'key': project.key,
                'organization': {
                    'id': project.organization.id,
                    'name': project.organization.name,
                    'slug': project.organization.slug
                },
                'created_at': project.created_at
            },
            'my_role': membership.role,
            'member_since': membership.created_at,
            'diagrams_count': len(diagrams_data),
            'diagrams': diagrams_data
        })
    
    return Response({
        'projects': projects_data,
        'total_projects': len(projects_data)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_diagrams(request, project_id):
    """Listar diagramas de un proyecto específico donde el usuario es miembro."""
    # Verificar que el proyecto existe y el usuario es miembro
    try:
        project = Project.objects.select_related('organization').get(id=project_id)
        membership = ProjectMember.objects.get(project=project, user=request.user)
    except Project.DoesNotExist:
        return Response({'error': 'Proyecto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except ProjectMember.DoesNotExist:
        return Response({'error': 'No eres miembro de este proyecto'}, status=status.HTTP_403_FORBIDDEN)
    
    # Obtener diagramas del proyecto
    diagrams = Diagram.objects.filter(project=project).select_related('created_by').order_by('name')
    
    diagrams_data = [
        {
            'id': diagram.id,
            'name': diagram.name,
            'current_version': diagram.current_version,
            'created_by': {
                'id': diagram.created_by.id,
                'username': diagram.created_by.username
            },
            'created_at': diagram.created_at,
            'updated_at': diagram.updated_at
        }
        for diagram in diagrams
    ]
    
    return Response({
        'project': {
            'id': project.id,
            'name': project.name,
            'key': project.key,
            'organization': {
                'id': project.organization.id,
                'name': project.organization.name,
                'slug': project.organization.slug
            }
        },
        'my_role': membership.role,
        'diagrams': diagrams_data,
        'total_diagrams': len(diagrams_data)
    })

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
        role='viewer'  # Rol más básico
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
            'email': member.user.email,
            'role': member.role,
            'joined_at': member.created_at
        }
        for member in members
    ]
    
    return Response({
        'project': {
            'id': diagram.project.id,
            'name': diagram.project.name,
            'key': diagram.project.key
        },
        'diagram': {
            'id': diagram.id,
            'name': diagram.name
        },
        'members': data,
        'total_members': len(data)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_diagrams(request):
    """
    DEPRECATED: Usar my_projects en su lugar.
    Mantenido por compatibilidad pero devuelve estructura mejorada.
    """
    # Obtener proyectos donde el usuario es miembro
    user_projects = ProjectMember.objects.filter(user=request.user).values_list('project_id', flat=True)
    
    # Obtener diagramas de esos proyectos organizados por proyecto
    projects_with_diagrams = {}
    diagrams = Diagram.objects.filter(
        project_id__in=user_projects
    ).select_related('project', 'project__organization', 'created_by').order_by('project__name', 'name')
    
    for diagram in diagrams:
        project_key = f"{diagram.project.organization.slug}/{diagram.project.key}"
        if project_key not in projects_with_diagrams:
            projects_with_diagrams[project_key] = {
                'project': {
                    'id': diagram.project.id,
                    'name': diagram.project.name,
                    'key': diagram.project.key,
                    'organization': diagram.project.organization.name
                },
                'diagrams': []
            }
        
        projects_with_diagrams[project_key]['diagrams'].append({
            'id': diagram.id,
            'name': diagram.name,
            'created_by': diagram.created_by.username,
            'created_at': diagram.created_at
        })
    
    return Response({
        'message': 'Considera usar /api/my-projects/ para mejor experiencia',
        'projects': list(projects_with_diagrams.values()),
        'total_projects': len(projects_with_diagrams)
    })