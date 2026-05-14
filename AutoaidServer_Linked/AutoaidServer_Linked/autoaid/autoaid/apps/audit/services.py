
from typing import Optional
from .models import AuditEvent


def audit_event(request, *, action: str, object_type: str = '', object_id: str = '', metadata: Optional[dict] = None):
    user = getattr(request, 'user', None)
    if user is not None and getattr(user, 'is_authenticated', False) is False:
        user = None

    ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR', '')
    ua = (request.META.get('HTTP_USER_AGENT', '') or '')[:256]
    rid = getattr(request, 'request_id', '')

    AuditEvent.objects.create(
        user=user,
        action=action,
        object_type=object_type,
        object_id=object_id,
        ip_address=ip,
        user_agent=ua,
        request_id=rid,
        metadata=metadata or {},
    )
