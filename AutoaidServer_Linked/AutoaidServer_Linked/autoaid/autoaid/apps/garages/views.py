
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Garage
from .serializers import GarageSerializer
from .services import haversine_km
from autoaid.apps.audit.services import audit_event

class NearbyGaragesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            lat = float(request.query_params.get('lat'))
            lon = float(request.query_params.get('lon'))
        except (TypeError, ValueError):
            return Response({"detail": "lat and lon query params are required"}, status=400)

        radius_km = float(request.query_params.get('radius_km', 10.0))
        garages = list(Garage.objects.all())

        enriched = []
        for g in garages:
            d = haversine_km(lat, lon, g.latitude, g.longitude)
            if d <= radius_km:
                g.distance_km = round(d, 3)
                enriched.append(g)

        enriched.sort(key=lambda x: x.distance_km)
        audit_event(request, action='GARAGE_NEARBY_QUERY', metadata={'lat': lat, 'lon': lon, 'radius_km': radius_km, 'count': len(enriched)})
        return Response(GarageSerializer(enriched, many=True).data)
