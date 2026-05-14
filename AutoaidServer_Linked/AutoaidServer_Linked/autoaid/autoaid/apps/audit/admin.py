
from django.contrib import admin
from .models import AuditEvent

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'object_type', 'object_id', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('object_id', 'user__email', 'request_id')
