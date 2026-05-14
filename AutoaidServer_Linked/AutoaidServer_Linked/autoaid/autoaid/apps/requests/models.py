
import uuid
from django.db import models
from django.conf import settings

from autoaid.apps.diagnostics.models import VehicleIssue
from autoaid.apps.garages.models import Garage

class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING'
        ACCEPTED = 'ACCEPTED'
        REJECTED = 'REJECTED'
        CANCELLED = 'CANCELLED'
        COMPLETED = 'COMPLETED'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='service_requests')
    issue = models.ForeignKey(VehicleIssue, on_delete=models.CASCADE, related_name='service_requests')
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='service_requests')

    notes = models.TextField(blank=True)
    preferred_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} ({self.status})"
