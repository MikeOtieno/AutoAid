
from django.urls import path
from .views import ServiceRequestCreateView

urlpatterns = [
    path('service-request/', ServiceRequestCreateView.as_view(), name='service-request-create'),
]
