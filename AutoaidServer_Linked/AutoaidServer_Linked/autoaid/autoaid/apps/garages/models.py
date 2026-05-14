
import uuid
from django.db import models

class Garage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    services = models.JSONField(default=list, blank=True)
    rating = models.FloatField(default=4.5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
