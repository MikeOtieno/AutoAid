import os
import base64
import uuid
import mimetypes
from io import BytesIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

from .models import VehicleIssue, UploadedMedia, DiagnosisResult


class DiagnoseRequestSerializer(serializers.Serializer):
    """
    Accepts JSON with base64-encoded images and audio from the Android app.

    Expected payload:
    {
        "problem_text": "my car won't start",
        "images": ["<base64>", "<base64>"],   // list of base64 strings
        "audio":  "<base64>"                   // single base64 string
    }
    """
    problem_text = serializers.CharField(required=False, allow_blank=True)
    callback_url = serializers.URLField(required=False, allow_blank=True, default='')

    # ✅ Accept base64 list for images (matches Android DiagnoseRequest.images)
    images = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        default=list,
    )

    # ✅ Accept base64 string for audio
    audio = serializers.CharField(required=False, allow_blank=True, allow_null=True, default=None)

    def validate(self, attrs):
        problem_text = (attrs.get('problem_text') or '').strip()
        images       = attrs.get('images') or []
        audio        = attrs.get('audio')

        if not problem_text and not images and not audio:
            raise serializers.ValidationError(
                'At least one of problem_text, images, or audio must be provided.')

        max_bytes = getattr(settings, 'MAX_UPLOAD_MB', 50) * 1024 * 1024

        # ── Decode and validate images ────────────────────────────────────────
        decoded_images = []
        for i, b64 in enumerate(images[:5]):  # max 5 images
            try:
                # Strip data URI prefix if present
                if ',' in b64:
                    b64 = b64.split(',', 1)[1]
                data = base64.b64decode(b64)
                if len(data) > max_bytes:
                    raise serializers.ValidationError(f'Image {i+1} too large')
                filename = f'upload_{uuid.uuid4().hex}.jpg'
                f = InMemoryUploadedFile(
                    file=BytesIO(data),
                    field_name='images',
                    name=filename,
                    content_type='image/jpeg',
                    size=len(data),
                    charset=None,
                )
                decoded_images.append(f)
            except Exception as e:
                raise serializers.ValidationError(f'Invalid image {i+1}: {e}')

        attrs['decoded_images'] = decoded_images

        # ── Decode and validate audio ─────────────────────────────────────────
        decoded_audio = None
        if audio:
            try:
                if ',' in audio:
                    audio = audio.split(',', 1)[1]
                data = base64.b64decode(audio)
                if len(data) > max_bytes:
                    raise serializers.ValidationError('Audio too large')
                filename = f'audio_{uuid.uuid4().hex}.wav'
                decoded_audio = InMemoryUploadedFile(
                    file=BytesIO(data),
                    field_name='audio',
                    name=filename,
                    content_type='audio/wav',
                    size=len(data),
                    charset=None,
                )
            except Exception as e:
                raise serializers.ValidationError(f'Invalid audio: {e}')

        attrs['decoded_audio'] = decoded_audio
        return attrs


class UploadedMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UploadedMedia
        fields = ('id', 'media_type', 'file', 'original_name',
                  'content_type', 'size_bytes', 'created_at')
        read_only_fields = fields


class DiagnosisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DiagnosisResult
        fields = ('id', 'diagnosis', 'confidence', 'recommended_action',
                  'possible_causes', 'requires_mechanic', 'explanation', 'created_at')


class VehicleIssueSerializer(serializers.ModelSerializer):
    media     = UploadedMediaSerializer(many=True, read_only=True)
    diagnosis = DiagnosisResultSerializer(read_only=True)

    class Meta:
        model  = VehicleIssue
        fields = ('id', 'problem_text', 'status', 'callback_url',
                  'callback_delivered_at', 'created_at', 'updated_at',
                  'media', 'diagnosis')
        read_only_fields = ('id', 'status', 'callback_delivered_at',
                            'created_at', 'updated_at', 'media', 'diagnosis')