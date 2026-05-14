
from django.urls import path, include

urlpatterns = [
    path('auth/', include('autoaid.apps.users.urls_auth')),
    path('', include('autoaid.apps.diagnostics.urls')),
    path('', include('autoaid.apps.garages.urls')),
    path('', include('autoaid.apps.requests.urls')),
]
