from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CreateUserView, CustomTokenObtainPairView

urlpatterns = [
    path('users/create/', CreateUserView.as_view(), name='user-create'),

    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
]