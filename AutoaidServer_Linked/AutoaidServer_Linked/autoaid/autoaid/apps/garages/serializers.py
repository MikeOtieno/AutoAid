
from rest_framework import serializers
from .models import Garage

class GarageSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = Garage
        fields = ('id', 'name', 'address', 'phone', 'email', 'latitude', 'longitude', 'services', 'rating', 'distance_km')
