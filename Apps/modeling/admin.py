from django.contrib import admin
from .models import Diagram, DiagramVersion, ModelClass, ModelAttribute, ModelMethod, EnumType, EnumValue, ModelRelation

# Registrar modelos relacionados con el modelado UML
admin.site.register(Diagram)
admin.site.register(DiagramVersion)
admin.site.register(ModelClass)
admin.site.register(ModelAttribute)
admin.site.register(ModelMethod)
admin.site.register(EnumType)
admin.site.register(EnumValue)
admin.site.register(ModelRelation)
