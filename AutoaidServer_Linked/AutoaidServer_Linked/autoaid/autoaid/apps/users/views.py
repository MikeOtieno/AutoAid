from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserCreateSerializer, CustomTokenObtainPairSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # ✅ Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # ✅ Match Android AuthResponse exactly
        return Response({
            "success": True,
            "message": "User created successfully",
            "accessToken": str(refresh.access_token),
            "refreshToken": str(refresh),

            "name": getattr(user, "name", ""),
            "email": user.email,
            "phone": getattr(user, "phone", "")
        }, status=status.HTTP_201_CREATED)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer