
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('autoaid.config.v1_urls')),
    path('api/schema/', include('autoaid.config.schema_urls')),
    path('health/', include('autoaid.config.health_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Android compatibility endpoints
from autoaid.config.mobile_compat import RegisterCompatView, LoginCompatView, DiagnoseCompatView, NearbyGaragesCompatView, BookingCompatView
urlpatterns += [
    path('api/auth/register', RegisterCompatView.as_view(), name='android-register'),
    path('api/auth/login', LoginCompatView.as_view(), name='android-login'),
    path('api/diagnostics/', DiagnoseCompatView.as_view(), name='android-diagnose'),
    path('api/garages/nearby', NearbyGaragesCompatView.as_view(), name='android-garages-nearby'),
    path('api/bookings/', BookingCompatView.as_view(), name='android-bookings'),
]
