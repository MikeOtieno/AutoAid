from rest_framework import serializers
from .models import User

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # optional extra claims inside JWT
        token['email'] = user.email
        token['name'] = getattr(user, 'name', '')
        token['phone'] = getattr(user, 'phone', '')

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # reshape response for Android
        return {
            "success": True,
            "message": "Login successful",

            "accessToken": data["access"],
            "refreshToken": data["refresh"],

            "name": getattr(self.user, "name", ""),
            "email": self.user.email,
            "phone": getattr(self.user, "phone", "")
        }