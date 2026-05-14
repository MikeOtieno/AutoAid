
from django.contrib import admin
from .models import Garage

@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'latitude', 'longitude')
    search_fields = ('name', 'address')
