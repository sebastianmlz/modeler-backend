from django.contrib import admin
from .models import Event, AuditLog, UsageStat, ErrorLog

# Registrar modelos relacionados con telemetría y auditoría
admin.site.register(Event)
admin.site.register(AuditLog)
admin.site.register(UsageStat)
admin.site.register(ErrorLog)
