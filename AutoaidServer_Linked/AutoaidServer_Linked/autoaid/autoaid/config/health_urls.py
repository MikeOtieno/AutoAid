
from django.urls import path
from autoaid.config.views import health

urlpatterns = [
    path('', health, name='health'),
]
