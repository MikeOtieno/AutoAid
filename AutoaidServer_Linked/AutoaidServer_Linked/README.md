
# AutoAid Backend (Django + DRF) – Production Grade

This repo is a **complete, scalable Django REST backend** for an AI-powered vehicle diagnostics mobile app.
It supports multi-modal inputs:

- **Image** (damage detection / segmentation) using VIA polygon annotations → YOLOv8/COCO tooling
- **Audio (.wav)** engine/vehicle state diagnostics via classification model
- **Text** symptom description (used as a prior + explainability)

It implements your mobile flow with:

- JWT auth
- File uploads
- Async inference (Celery + Redis)
- Confidence threshold logic and escalation rules
- Garages nearby + service request
- Refresh/re-run inference endpoint
- Optional webhooks (push result to mobile)
- Rate limiting + audit logging

---

## Quick Start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

Initialize DB:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Swagger UI:
- http://localhost:8000/api/schema/swagger/

Health:
- http://localhost:8000/health/

---

## API (v1)

### Auth
- `POST /api/v1/auth/jwt/create/`
- `POST /api/v1/auth/jwt/refresh/`

### Diagnosis Flow
- `POST /api/v1/diagnose/` *(multipart)* → returns `issue_id` (async)
- `GET  /api/v1/diagnosis/{id}/` → returns status + contract response when complete
- `POST /api/v1/diagnosis/{id}/refresh/` → re-run inference (e.g. after new uploads)

### Garages
- `GET  /api/v1/garages/nearby/?lat=...&lon=...&radius_km=...`

### Service Requests
- `POST /api/v1/service-request/`

---

## Diagnose request (multipart)

```bash
curl -X POST http://localhost:8000/api/v1/diagnose/   -H "Authorization: Bearer <JWT>"   -F "problem_text=Car makes squealing noise when braking"   -F "callback_url=https://your.mobile.app/webhook/autoaid"   -F "image=@/path/to/photo.jpg"   -F "audio=@/path/to/recording.wav"
```

Response (202):
```json
{ "issue_id": "<uuid>", "status": "PROCESSING" }
```

Fetch result:
```bash
curl -H "Authorization: Bearer <JWT>" http://localhost:8000/api/v1/diagnosis/<uuid>/
```

Contract payload under `diagnosis_contract` when completed:
```json
{
  "diagnosis": "...",
  "confidence": 0.92,
  "recommended_action": "...",
  "possible_causes": ["..."],
  "requires_mechanic": true,
  "explanation": {"fusion": {"evidence": [...]}}
}
```

---

## Webhook callbacks (optional)

If `callback_url` is provided on `/diagnose/`, worker will POST:

```json
{
  "issue_id": "<uuid>",
  "status": "COMPLETED",
  "result": {
    "diagnosis": "...",
    "confidence": 0.92,
    "recommended_action": "...",
    "possible_causes": [],
    "requires_mechanic": true,
    "explanation": {...}
  }
}
```

Security: You can enable signed webhooks by setting `WEBHOOK_SECRET` and verifying HMAC signature header `X-AutoAid-Signature`.

---

## Rate limiting

Default throttles (
- burst: 30/min
- sustained: 300/day
) are configured in settings.

---

## ML toolchain

### Image: VIA JSON → YOLOv8 segmentation

```bash
python ml/training/image/via_to_yolo_seg.py   --via_train /data/0Train_via_annos.json   --via_val /data/0Val_via_annos.json   --images_dir /data/image/image   --out_dir /data_yolo
```

Train:
```bash
yolo task=segment mode=train model=yolov8n-seg.pt data=/data_yolo/dataset.yaml epochs=100 imgsz=640
```

Export ONNX:
```bash
yolo mode=export model=runs/segment/train/weights/best.pt format=onnx
```

Mount to container as `/models/image/best.onnx` and set `IMAGE_MODEL_PATH`.

### Audio: WAV classification

Manifest:
```bash
python ml/training/audio/prepare_manifest.py --root_dir "/data/car diagnostics dataset" --out manifest.csv
```

Train:
```bash
python ml/training/audio/train_audio_cnn.py --manifest manifest.csv --out_dir audio_runs --epochs 50
```

Mount `/models/audio/best.pt` and set `AUDIO_MODEL_PATH`.

---

## Production deployment notes

- Nginx in front of Gunicorn
- Postgres + Redis
- Celery worker(s) scale horizontally
- Uploads can be switched to S3/GCS by changing storage backend
- Add observability (Sentry/OpenTelemetry) easily via middleware hooks

