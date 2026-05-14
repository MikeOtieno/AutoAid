
from .services import audit_event

SAFE_METHODS = {'GET', 'HEAD', 'OPTIONS'}

class AuditMiddleware:
    """Captures basic request context. Explicit business events are logged from services/views."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # We do not log every request to avoid noise; but you can enable it by uncommenting below.
        # if request.method not in SAFE_METHODS:
        #     audit_event(request, action='HTTP_' + request.method, metadata={'path': request.path, 'status': response.status_code})
        return response
