
import hashlib
import hmac
import json
import urllib.request
from django.conf import settings


def post_webhook(url: str, payload: dict):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url=url, data=data, method='POST')
    req.add_header('Content-Type', 'application/json')

    # Optional signing
    if settings.WEBHOOK_SECRET:
        sig = hmac.new(settings.WEBHOOK_SECRET.encode('utf-8'), data, hashlib.sha256).hexdigest()
        req.add_header('X-AutoAid-Signature', sig)

    timeout = getattr(settings, 'WEBHOOK_TIMEOUT_SECONDS', 8)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        _ = resp.read()
        return resp.status
