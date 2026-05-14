"""Compatibility endpoints for the existing Android app.
These endpoints keep the Android frontend simple while using the Django/DRF server models.
"""
from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from autoaid.apps.users.models import User
from autoaid.apps.diagnostics.models import VehicleIssue, DiagnosisResult
from autoaid.apps.garages.models import Garage
from autoaid.apps.requests.models import ServiceRequest
from autoaid.apps.ml_engine.services.predictor import Predictor
from autoaid.apps.garages.services import haversine_km


def token_payload(user, message="OK", created=False):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    return {
        "success": True,
        "message": message,
        "access_token": access,
        "accessToken": access,
        "refresh_token": str(refresh),
        "refreshToken": str(refresh),
        "token_type": "bearer",
        "name": getattr(user, "name", "") or "",
        "email": user.email,
        "phone": getattr(user, "phone", "") or "",
        "user": {
            "id": str(user.id),
            "full_name": getattr(user, "name", "") or "",
            "name": getattr(user, "name", "") or "",
            "email": user.email,
            "phone": getattr(user, "phone", "") or "",
            "role": "driver",
        }
    }


class RegisterCompatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""
        name = (request.data.get("full_name") or request.data.get("name") or "").strip()
        phone = (request.data.get("phone") or "").strip()
        if not email or not password:
            return Response({"success": False, "message": "Email and password are required"}, status=400)
        if User.objects.filter(email=email).exists():
            return Response({"success": False, "message": "Email already exists"}, status=400)
        user = User.objects.create_user(email=email, password=password, name=name, phone=phone)
        return Response(token_payload(user, "User created successfully", True), status=201)


class LoginCompatView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        password = request.data.get("password") or ""
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"success": False, "message": "Invalid email or password"}, status=401)
        return Response(token_payload(user, "Login successful"), status=200)


def diagnosis_to_android(issue, diagnosis):
    confidence = float(diagnosis.confidence or 0.0)
    urgency = "critical" if confidence >= 0.80 and diagnosis.requires_mechanic else "high" if diagnosis.requires_mechanic else "medium"
    predictions = []
    for cause in diagnosis.possible_causes or []:
        predictions.append({"fault": cause, "confidence": confidence, "urgency": urgency})
    if not predictions:
        predictions = [{"fault": diagnosis.diagnosis, "confidence": confidence, "urgency": urgency}]
    return {
        "id": str(issue.id),
        "issue_id": str(issue.id),
        "problem": diagnosis.diagnosis,
        "top_fault": diagnosis.diagnosis,
        "top_confidence": confidence,
        "confidence": round(confidence * 100),
        "urgency": urgency,
        "predictions": predictions,
        "recommendedAction": diagnosis.recommended_action,
        "recommended_action": diagnosis.recommended_action,
        "status": issue.status,
    }


class DiagnoseCompatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Android currently sends multipart text_description. Server also accepts problem_text.
        text = (request.data.get("text_description") or request.data.get("problem_text") or "").strip()
        if not text:
            return Response({"detail": "text_description is required"}, status=400)
        predictor = Predictor()
        result = predictor.predict(image_path=None, audio_path=None, text=text)
        with transaction.atomic():
            issue = VehicleIssue.objects.create(user=request.user, problem_text=text, status=VehicleIssue.Status.COMPLETED)
            diagnosis = DiagnosisResult.objects.create(
                issue=issue,
                diagnosis=result["diagnosis"],
                confidence=result["confidence"],
                recommended_action=result["recommended_action"],
                possible_causes=result.get("possible_causes", []),
                requires_mechanic=result.get("requires_mechanic", False),
                explanation=result.get("explanation", {}),
            )
        return Response(diagnosis_to_android(issue, diagnosis), status=201)


class NearbyGaragesCompatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            lat = float(request.query_params.get("lat"))
            lon = float(request.query_params.get("lon"))
        except (TypeError, ValueError):
            return Response({"detail": "lat and lon are required"}, status=400)
        radius_km = float(request.query_params.get("radius_km", 50.0))
        out = []
        for g in Garage.objects.all():
            d = haversine_km(lat, lon, g.latitude, g.longitude)
            if d <= radius_km:
                services = g.services or []
                out.append({
                    "id": str(g.id),
                    "name": g.name,
                    "address": g.address,
                    "phone": g.phone,
                    "email": g.email,
                    "latitude": g.latitude,
                    "longitude": g.longitude,
                    "rating": g.rating,
                    "price_range": "KES 1,500 - 8,000",
                    "specializations": services,
                    "services": services,
                    "specialization": ", ".join(services),
                    "distance_km": round(d, 2),
                })
        out.sort(key=lambda x: x["distance_km"])
        return Response(out)


class BookingCompatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        garage_id = request.data.get("garage_id") or request.data.get("garage")
        if not garage_id:
            return Response({"success": False, "message": "garage_id is required"}, status=400)
        try:
            garage = Garage.objects.get(id=garage_id)
        except Garage.DoesNotExist:
            return Response({"success": False, "message": "Garage not found"}, status=404)
        issue = None
        diagnostic_id = request.data.get("diagnostic_id") or request.data.get("issue")
        if diagnostic_id:
            issue = VehicleIssue.objects.filter(id=diagnostic_id, user=request.user).first()
        if issue is None:
            # Create a lightweight issue so the ServiceRequest FK is satisfied.
            notes = request.data.get("notes") or request.data.get("problemSummary") or "Garage booking request"
            issue = VehicleIssue.objects.create(user=request.user, problem_text=notes, status=VehicleIssue.Status.COMPLETED)
        service_type = request.data.get("service_type") or "garage_visit"
        notes = request.data.get("notes") or f"Service type: {service_type}"
        obj = ServiceRequest.objects.create(user=request.user, issue=issue, garage=garage, notes=notes)
        return Response({"success": True, "message": "Booking submitted successfully", "id": str(obj.id), "status": obj.status}, status=201)
