import logging
import os
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .models import VehicleIssue, UploadedMedia
from .serializers import DiagnoseRequestSerializer, VehicleIssueSerializer
from autoaid.apps.ml_engine.tasks import run_diagnosis_task
from autoaid.apps.audit.services import audit_event

logger = logging.getLogger(__name__)


def save_file_directly(in_memory_file, subfolder):
    """
    Save an InMemoryUploadedFile directly to disk without Django storage.
    Returns the absolute file path.
    """
    media_root = getattr(settings, 'MEDIA_ROOT', None) or os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'media'
    )
    save_dir = os.path.join(media_root, subfolder)
    os.makedirs(save_dir, exist_ok=True)

    ext      = os.path.splitext(in_memory_file.name)[1].lower() or '.jpg'
    filename = uuid.uuid4().hex + ext
    filepath = os.path.join(save_dir, filename)

    with open(filepath, 'wb') as f:
        in_memory_file.seek(0)
        f.write(in_memory_file.read())

    logger.info('Saved file directly: %s (%d bytes)', filepath, os.path.getsize(filepath))
    return filepath


class DiagnoseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = DiagnoseRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        issue = VehicleIssue.objects.create(
            user=request.user,
            problem_text=(data.get('problem_text') or '').strip(),
            status=VehicleIssue.Status.RECEIVED,
            callback_url=(data.get('callback_url') or '').strip(),
        )

        # Save images directly to disk — bypasses Django storage backslash bug
        decoded_images = data.get('decoded_images') or []
        for f in decoded_images:
            try:
                subfolder = 'uploads/{}/{}/image'.format(
                    str(issue.user_id), str(issue.id))
                filepath = save_file_directly(f, subfolder)

                media_root = getattr(settings, 'MEDIA_ROOT', '')
                rel_path   = os.path.relpath(filepath, media_root).replace('\\', '/')

                UploadedMedia.objects.create(
                    issue=issue,
                    media_type=UploadedMedia.MediaType.IMAGE,
                    file=rel_path,
                    original_name=f.name[:255],
                    content_type='image/jpeg',
                    size_bytes=f.size,
                )
                logger.info('Image saved: %s', rel_path)
            except Exception as e:
                logger.warning('Failed to save image: %s', e)

        # Save audio directly to disk
        decoded_audio = data.get('decoded_audio')
        if decoded_audio:
            try:
                subfolder = 'uploads/{}/{}/audio'.format(
                    str(issue.user_id), str(issue.id))
                filepath = save_file_directly(decoded_audio, subfolder)

                media_root = getattr(settings, 'MEDIA_ROOT', '')
                rel_path   = os.path.relpath(filepath, media_root).replace('\\', '/')

                UploadedMedia.objects.create(
                    issue=issue,
                    media_type=UploadedMedia.MediaType.AUDIO,
                    file=rel_path,
                    original_name=decoded_audio.name[:255],
                    content_type='audio/wav',
                    size_bytes=decoded_audio.size,
                )
                logger.info('Audio saved: %s', rel_path)
            except Exception as e:
                logger.warning('Failed to save audio: %s', e)

        logger.info('Issue %s — images: %d, audio: %s, text: %s',
                    issue.id,
                    len(decoded_images),
                    'yes' if decoded_audio else 'no',
                    'yes' if issue.problem_text else 'no')

        issue.status = VehicleIssue.Status.PROCESSING
        issue.save(update_fields=['status', 'updated_at'])
        run_diagnosis_task.delay(str(issue.id))

        audit_event(request, action='ISSUE_CREATED',
                    object_type='VehicleIssue', object_id=str(issue.id))
        return Response({"issue_id": str(issue.id), "status": issue.status}, status=202)


class DiagnosisDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            issue = VehicleIssue.objects.select_related('diagnosis')\
                        .prefetch_related('media')\
                        .get(id=id, user=request.user)
        except VehicleIssue.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        payload = VehicleIssueSerializer(issue).data

        if issue.status == VehicleIssue.Status.COMPLETED and hasattr(issue, 'diagnosis'):
            d = issue.diagnosis
            payload['diagnosis_contract'] = {
                "diagnosis":          d.diagnosis,
                "confidence":         d.confidence,
                "recommended_action": d.recommended_action,
                "possible_causes":    d.possible_causes,
                "requires_mechanic":  d.requires_mechanic,
                "explanation":        d.explanation,
            }

        audit_event(request, action='DIAGNOSIS_FETCH',
                    object_type='VehicleIssue', object_id=str(id),
                    metadata={'status': issue.status})
        return Response(payload)


class DiagnosisRefreshView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            issue = VehicleIssue.objects.get(id=id, user=request.user)
        except VehicleIssue.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        issue.status = VehicleIssue.Status.PROCESSING
        issue.save(update_fields=['status', 'updated_at'])
        run_diagnosis_task.delay(str(issue.id))

        audit_event(request, action='DIAGNOSIS_REFRESH',
                    object_type='VehicleIssue', object_id=str(id))
        return Response({"issue_id": str(issue.id), "status": issue.status}, status=202)
