
from django.urls import path
from .views import DiagnoseView, DiagnosisDetailView, DiagnosisRefreshView

urlpatterns = [
    path('diagnose/', DiagnoseView.as_view(), name='diagnose'),
    path('diagnosis/<uuid:id>/', DiagnosisDetailView.as_view(), name='diagnosis-detail'),
    path('diagnosis/<uuid:id>/refresh/', DiagnosisRefreshView.as_view(), name='diagnosis-refresh'),
]
