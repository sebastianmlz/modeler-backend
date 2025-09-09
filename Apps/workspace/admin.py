from django.contrib import admin
from .models import Organization, Membership, Invite, Project, ProjectMember

# Registrar modelos relacionados con organizaciones y proyectos
admin.site.register(Organization)
admin.site.register(Membership)
admin.site.register(Invite)
admin.site.register(Project)
admin.site.register(ProjectMember)
