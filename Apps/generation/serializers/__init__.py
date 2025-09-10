"""
Serializers para generación de código.
"""
from rest_framework import serializers
from ..models import Template, GenerationJob, StorageRef, Artifact, GenerationLog, SwaggerSpec


class TemplateSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Template."""
    
    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class GenerationJobSerializer(serializers.ModelSerializer):
    """Serializer para el modelo GenerationJob."""
    
    class Meta:
        model = GenerationJob
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'started_at', 'finished_at']


class StorageRefSerializer(serializers.ModelSerializer):
    """Serializer para el modelo StorageRef."""
    
    class Meta:
        model = StorageRef
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class ArtifactSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Artifact."""
    
    class Meta:
        model = Artifact
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class GenerationLogSerializer(serializers.ModelSerializer):
    """Serializer para el modelo GenerationLog."""
    
    class Meta:
        model = GenerationLog
        fields = '__all__'
        read_only_fields = ['id']


class SwaggerSpecSerializer(serializers.ModelSerializer):
    """Serializer para el modelo SwaggerSpec."""
    
    class Meta:
        model = SwaggerSpec
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
