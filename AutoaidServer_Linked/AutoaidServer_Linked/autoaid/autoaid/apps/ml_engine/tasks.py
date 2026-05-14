import os
import logging
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from autoaid.apps.diagnostics.models import VehicleIssue, DiagnosisResult, UploadedMedia
from autoaid.apps.ml_engine.services.predictor import Predictor
from autoaid.apps.ml_engine.services.webhook import post_webhook
from autoaid.apps.audit.services import audit_event

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def run_diagnosis_task(self, issue_id: str):
    try:
        issue = VehicleIssue.objects.prefetch_related('media').get(id=issue_id)
        logger.info('MEDIA COUNT: %d', issue.media.count())
        for m in issue.media.all():
           logger.info('MEDIA: type=%s path=%s exists=%s',
        m.media_type, m.file.path,
        os.path.exists(m.file.path) if m.file else False)   
           
        
        image_path = None
        audio_path = None
        for m in issue.media.all():
            if m.media_type == UploadedMedia.MediaType.IMAGE:
                image_path = m.file.path
            elif m.media_type == UploadedMedia.MediaType.AUDIO:
                audio_path = m.file.path

        predictor = Predictor()
        result = predictor.predict(image_path=image_path, audio_path=audio_path, text=issue.problem_text)

        '''with transaction.atomic():
            DiagnosisResult.objects.update_or_create(
                issue=issue,
                defaults={
                    'diagnosis': result['diagnosis'],
                    'confidence': result['confidence'],
                    'recommended_action': result['recommended_action'],
                    'possible_causes': result['possible_causes'],
                    'requires_mechanic': result['requires_mechanic'],
                    'explanation': result.get('explanation', {}),
                }
            )
            issue.status = VehicleIssue.Status.COMPLETED
            issue.save(update_fields=['status', 'updated_at'])'''
        # Use get+save instead of update_or_create to avoid
        # select_for_update deadlock on SQLite with ALWAYS_EAGER
        try:
            diagnosis_result = DiagnosisResult.objects.get(issue=issue)
            diagnosis_result.diagnosis          = result['diagnosis']
            diagnosis_result.confidence         = result['confidence']
            diagnosis_result.recommended_action = result['recommended_action']
            diagnosis_result.possible_causes    = result['possible_causes']
            diagnosis_result.requires_mechanic  = result['requires_mechanic']
            diagnosis_result.explanation        = result.get('explanation', {})
            diagnosis_result.save()
        except DiagnosisResult.DoesNotExist:
            DiagnosisResult.objects.create(
                issue               = issue,
                diagnosis           = result['diagnosis'],
                confidence          = result['confidence'],
                recommended_action  = result['recommended_action'],
                possible_causes     = result['possible_causes'],
                requires_mechanic   = result['requires_mechanic'],
                explanation         = result.get('explanation', {}),
            )

        issue.status = VehicleIssue.Status.COMPLETED
        issue.save(update_fields=['status', 'updated_at'])

        # Attempt webhook delivery
        if issue.callback_url:
            payload = {
                'issue_id': str(issue.id),
                'status': issue.status,
                'result': result,
            }
            try:
                status_code = post_webhook(issue.callback_url, payload)
                issue.callback_delivered_at = timezone.now()
                issue.save(update_fields=['callback_delivered_at'])
                logger.info('Webhook delivered (%s) for %s', status_code, issue_id)
            except Exception as e:
                logger.warning('Webhook delivery failed for %s: %s', issue_id, e)

        logger.info('Diagnosis complete for %s', issue_id)
        return True

    except Exception as e:
        logger.exception('Diagnosis failed for %s: %s', issue_id, e)
        try:
            issue = VehicleIssue.objects.get(id=issue_id)
            issue.status = VehicleIssue.Status.FAILED
            issue.save(update_fields=['status', 'updated_at'])
        except Exception:
            pass
        raise
