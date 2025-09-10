"""
ViewSets para generación de código.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Template, GenerationJob, StorageRef, Artifact, GenerationLog, SwaggerSpec
from ..serializers import (
    TemplateSerializer, GenerationJobSerializer, StorageRefSerializer,
    ArtifactSerializer, GenerationLogSerializer, SwaggerSpecSerializer
)


class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para plantillas."""
    
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GenerationJobViewSet(viewsets.ModelViewSet):
    """ViewSet para trabajos de generación."""
    
    queryset = GenerationJob.objects.all()
    serializer_class = GenerationJobSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar trabajos por proyectos accesibles al usuario."""
        user = self.request.user
        if user.is_superuser:
            return GenerationJob.objects.all()
        
        return GenerationJob.objects.filter(
            project__organization__membership__user=user,
            project__organization__membership__status='active'
        )
    
    def perform_create(self, serializer):
        """Establecer el solicitante al usuario actual."""
        serializer.save(requester=self.request.user)
    
    @action(detail=True, methods=['get'])
    def artifacts(self, request, pk=None):
        """Obtener artefactos del trabajo."""
        job = self.get_object()
        artifacts = Artifact.objects.filter(job=job)
        serializer = ArtifactSerializer(artifacts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        """Obtener logs del trabajo."""
        job = self.get_object()
        logs = GenerationLog.objects.filter(job=job).order_by('ts')
        serializer = GenerationLogSerializer(logs, many=True)
        return Response(serializer.data)


class StorageRefViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para referencias de almacenamiento."""
    
    queryset = StorageRef.objects.all()
    serializer_class = StorageRefSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArtifactViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para artefactos."""
    
    queryset = Artifact.objects.all()
    serializer_class = ArtifactSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar artefactos por trabajos accesibles al usuario."""
        user = self.request.user
        if user.is_superuser:
            return Artifact.objects.all()
        
        return Artifact.objects.filter(
            job__project__organization__membership__user=user,
            job__project__organization__membership__status='active'
        )


class GenerationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para logs de generación."""
    
    queryset = GenerationLog.objects.all()
    serializer_class = GenerationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar logs por trabajos accesibles al usuario."""
        user = self.request.user
        if user.is_superuser:
            return GenerationLog.objects.all()
        
        return GenerationLog.objects.filter(
            job__project__organization__membership__user=user,
            job__project__organization__membership__status='active'
        )


class SwaggerSpecViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para especificaciones Swagger."""
    
    queryset = SwaggerSpec.objects.all()
    serializer_class = SwaggerSpecSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar especificaciones por trabajos accesibles al usuario."""
        user = self.request.user
        if user.is_superuser:
            return SwaggerSpec.objects.all()
        
        return SwaggerSpec.objects.filter(
            job__project__organization__membership__user=user,
            job__project__organization__membership__status='active'
        )
