
from django.contrib import admin
from .models import VehicleIssue, UploadedMedia, DiagnosisResult

@admin.register(VehicleIssue)
class VehicleIssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'callback_url', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'user__email')

@admin.register(UploadedMedia)
class UploadedMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'media_type', 'original_name', 'size_bytes', 'created_at')

@admin.register(DiagnosisResult)
class DiagnosisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'diagnosis', 'confidence', 'requires_mechanic', 'created_at')
