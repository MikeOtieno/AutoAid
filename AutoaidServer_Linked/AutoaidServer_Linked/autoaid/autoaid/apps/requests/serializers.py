
from rest_framework import serializers
from .models import ServiceRequest

class ServiceRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ('issue', 'garage', 'notes', 'preferred_time')

    def validate(self, attrs):
        user = self.context['request'].user
        issue = attrs.get('issue')
        if issue.user_id != user.id:
            raise serializers.ValidationError('Issue does not belong to the authenticated user.')
        return attrs

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ('id', 'user', 'issue', 'garage', 'notes', 'preferred_time', 'status', 'created_at')
        read_only_fields = fields
