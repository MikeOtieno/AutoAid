
from django.contrib import admin
from .models import ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'garage', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('id', 'user__email', 'garage__name')
