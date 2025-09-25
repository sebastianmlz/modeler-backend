"""
Serializers para las versiones de diagramas.
"""
from rest_framework import serializers
from django.db import transaction
from Apps.modeling.models import DiagramVersion, Diagram


class DiagramVersionSerializer(serializers.ModelSerializer):
    """Serializer para crear y listar versiones de diagramas (M04, M05)."""
    
    diagram_id = serializers.UUIDField(write_only=True, required=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    diagram_name = serializers.CharField(source='diagram.name', read_only=True)

    class Meta:
        model = DiagramVersion
        fields = [
            'id', 'diagram_id', 'version_number', 'snapshot', 'message',
            'created_by', 'created_by_username', 'diagram_name', 'created_at'
        ]
        read_only_fields = ['id', 'version_number', 'created_by', 'created_at', 
                           'created_by_username', 'diagram_name']

    def validate_snapshot(self, value):
        """Valida que el snapshot tenga estructura JSON válida."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("El snapshot debe ser un objeto JSON válido")
        
        # Validar estructura básica del snapshot según Fase 1
        required_fields = ['classes', 'relations', 'metadata']
        for field in required_fields:
            if field not in value:
                raise serializers.ValidationError(f"El snapshot debe contener el campo '{field}'")
        
        # Validar que classes sea una lista
        if not isinstance(value['classes'], list):
            raise serializers.ValidationError("El campo 'classes' debe ser una lista")
        
        # Validar que relations sea una lista
        if not isinstance(value['relations'], list):
            raise serializers.ValidationError("El campo 'relations' debe ser una lista")
        
        # Validar que metadata sea un objeto
        if not isinstance(value['metadata'], dict):
            raise serializers.ValidationError("El campo 'metadata' debe ser un objeto")
        
        return value

    def validate_diagram_id(self, value):
        """Valida que el diagrama exista y el usuario tenga permisos."""
        user = self.context['request'].user

        try:
            diagram = Diagram.objects.get(id=value)
        except Diagram.DoesNotExist:
            raise serializers.ValidationError("El diagrama especificado no existe")

        # Verificar que el usuario sea miembro del proyecto del diagrama
        from Apps.workspace.models import ProjectMember
        if not ProjectMember.objects.filter(
            project=diagram.project,
            user=user
        ).exists():
            raise serializers.ValidationError("No tienes permisos para crear versiones en este diagrama")

        # Verificar que el diagrama no esté eliminado
        if hasattr(diagram, 'deleted_at') and diagram.deleted_at is not None:
            raise serializers.ValidationError("No se pueden crear versiones de un diagrama eliminado")

        return value

    def validate_message(self, value):
        """Valida el mensaje de la versión."""
        if value and len(value.strip()) == 0:
            raise serializers.ValidationError("El mensaje no puede estar vacío")
        
        if value and len(value) > 240:
            raise serializers.ValidationError("El mensaje no puede exceder 240 caracteres")
        
        return value.strip() if value else None

    def create(self, validated_data):
        """Crea una nueva versión del diagrama con número de versión secuencial."""
        diagram_id = validated_data.pop('diagram_id')
        
        with transaction.atomic():
            # Obtener el diagrama
            diagram = Diagram.objects.select_for_update().get(id=diagram_id)
            
            # Obtener el siguiente número de versión
            last_version = DiagramVersion.objects.filter(diagram=diagram).order_by('-version_number').first()
            next_version_number = (last_version.version_number + 1) if last_version else 1
            
            # Crear la nueva versión (created_by ya viene en validated_data desde el viewset)
            diagram_version = DiagramVersion.objects.create(
                diagram=diagram,
                version_number=next_version_number,
                **validated_data
            )
            
            return diagram_version


class DiagramVersionDetailSerializer(serializers.ModelSerializer):
    """Serializer para obtener detalles de una versión específica (M06)."""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    diagram_name = serializers.CharField(source='diagram.name', read_only=True)
    diagram_id = serializers.UUIDField(source='diagram.id', read_only=True)
    project_name = serializers.CharField(source='diagram.project.name', read_only=True)
    project_id = serializers.UUIDField(source='diagram.project.id', read_only=True)
    
    class Meta:
        model = DiagramVersion
        fields = [
            'id', 'diagram_id', 'diagram_name', 'project_id', 'project_name',
            'version_number', 'snapshot', 'message', 'created_by',
            'created_by_username', 'created_by_email', 'created_at'
        ]
        read_only_fields = [
            'id', 'diagram_id', 'diagram_name', 'project_id', 'project_name',
            'version_number', 'snapshot', 'message', 'created_by',
            'created_by_username', 'created_by_email', 'created_at'
        ]


class DiagramVersionListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar versiones sin el snapshot completo."""
    
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    diagram_name = serializers.CharField(source='diagram.name', read_only=True)
    snapshot_size = serializers.SerializerMethodField()
    
    class Meta:
        model = DiagramVersion
        fields = [
            'id', 'version_number', 'message', 'created_by_username',
            'diagram_name', 'snapshot_size', 'created_at'
        ]
        read_only_fields = [
            'id', 'version_number', 'message', 'created_by_username',
            'diagram_name', 'snapshot_size', 'created_at'
        ]
    
    def get_snapshot_size(self, obj):
        """Retorna el tamaño del snapshot en elementos."""
        if not obj.snapshot:
            return 0
        
        classes_count = len(obj.snapshot.get('classes', []))
        relations_count = len(obj.snapshot.get('relations', []))
        
        return {
            'classes': classes_count,
            'relations': relations_count,
            'total_elements': classes_count + relations_count
        }
