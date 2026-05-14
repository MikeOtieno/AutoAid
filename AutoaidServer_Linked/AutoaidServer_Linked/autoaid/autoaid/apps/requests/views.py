
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ServiceRequestCreateSerializer, ServiceRequestSerializer
from autoaid.apps.audit.services import audit_event

class ServiceRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = ServiceRequestCreateSerializer(data=request.data, context={'request': request})
        ser.is_valid(raise_exception=True)
        obj = ser.save(user=request.user)
        audit_event(request, action='SERVICE_REQUEST_CREATED', object_type='ServiceRequest', object_id=str(obj.id))
        return Response(ServiceRequestSerializer(obj).data, status=201)
