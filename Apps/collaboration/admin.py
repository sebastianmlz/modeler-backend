from django.contrib import admin
from .models import CollabSession, Presence, Comment

# Registrar modelos relacionados con colaboración en tiempo real
admin.site.register(CollabSession)
admin.site.register(Presence)
admin.site.register(Comment)
