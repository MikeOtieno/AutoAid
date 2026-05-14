
import logging
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get('request')
    rid = getattr(request, 'request_id', '-') if request else '-'

    if response is not None:
        response.data['request_id'] = rid
    else:
        logger.exception('Unhandled exception [request_id=%s]: %s', rid, exc)

    return response
