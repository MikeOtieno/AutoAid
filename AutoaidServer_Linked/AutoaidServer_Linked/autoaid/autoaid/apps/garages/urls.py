
from django.urls import path
from .views import NearbyGaragesView

urlpatterns = [
    path('garages/nearby/', NearbyGaragesView.as_view(), name='garages-nearby'),
]
