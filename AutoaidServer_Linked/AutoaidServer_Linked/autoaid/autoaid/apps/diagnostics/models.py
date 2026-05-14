
import uuid
import os
from django.db import models
from django.conf import settings


def issue_upload_path(instance, filename: str):
    ext = os.path.splitext(filename)[1].lower() or '.jpg'
    rand = uuid.uuid4().hex
    user_id = str(instance.issue.user_id)
    issue_id = str(instance.issue_id)
    media_type = instance.media_type.lower()
    path = 'uploads/{}/{}/{}/{}{}'.format(user_id, issue_id, media_type, rand, ext)
    return path.replace('\\', '/')


class VehicleIssue(models.Model):
    class Status(models.TextChoices):
        RECEIVED = 'RECEIVED'
        PROCESSING = 'PROCESSING'
        COMPLETED = 'COMPLETED'
        FAILED = 'FAILED'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issues')

    problem_text = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.RECEIVED)

    # Optional callback URL (webhook)
    callback_url = models.URLField(blank=True)
    callback_delivered_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} ({self.status})"


class UploadedMedia(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'IMAGE'
        AUDIO = 'AUDIO'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(VehicleIssue, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=8, choices=MediaType.choices)

    file = models.FileField(upload_to=issue_upload_path)
    original_name = models.CharField(max_length=512, blank=True)
    content_type = models.CharField(max_length=128, blank=True)
    size_bytes = models.BigIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class DiagnosisResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.OneToOneField(VehicleIssue, on_delete=models.CASCADE, related_name='diagnosis')

    diagnosis = models.CharField(max_length=255)
    confidence = models.FloatField()
    recommended_action = models.CharField(max_length=255)
    possible_causes = models.JSONField(default=list)
    requires_mechanic = models.BooleanField(default=False)
    explanation = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
