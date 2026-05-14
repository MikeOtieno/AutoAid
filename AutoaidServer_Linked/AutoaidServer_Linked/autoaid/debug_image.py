"""
Run this to test the image model directly with the side_dent.jpeg file.
Copy side_dent.jpeg into your project folder first, then run:
    python debug_image.py
"""
import sys, os
sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'autoaid.config.settings.development'
import django
django.setup()

from django.conf import settings
from autoaid.apps.ml_engine.services.image_infer import ImageInferenceService
from autoaid.apps.ml_engine.services.predictor import Predictor
import cv2
import numpy as np

print("=" * 60)
print("IMAGE MODEL DIRECT TEST")
print("=" * 60)

# ── Test 1: Direct file path ──────────────────────────────────────────────────
image_path = 'side_dent.jpeg'
if not os.path.exists(image_path):
    print(f"ERROR: {image_path} not found — copy it to the project folder first")
    sys.exit(1)

svc = ImageInferenceService(settings.IMAGE_MODEL_PATH)
result = svc.predict(image_path)
print("TOP LABEL     :", result['top_label'])
print("TOP CONFIDENCE:", result['top_confidence'])
print("ALL SCORES    :")
for part, score in result.get('all_scores', {}).items():
    print(f"   {score:.4f}  {part}")

print()
print("=" * 60)
print("FULL PREDICTOR TEST (image only)")
print("=" * 60)
predictor = Predictor()
fused = predictor.predict(
    image_path=image_path,
    audio_path=None,
    text='my car was involved in an accident',
)
print("DIAGNOSIS  :", fused['diagnosis'])
print("CONFIDENCE :", fused['confidence'])
print("EVIDENCE   :")
for e in fused['explanation']['fusion']['evidence']:
    print(f"   [{e['source']}] {e['label']} — {e['confidence']:.2%}")

print()
print("=" * 60)
print("IMAGE QUALITY CHECK")
print("=" * 60)
img = cv2.imread(image_path)
print("Shape     :", img.shape)
print("Min/Max   :", img.min(), img.max())
print("File size :", os.path.getsize(image_path), "bytes")

# ── Test 2: Simulate what the Android app sends (base64 → decode → predict) ──
print()
print("=" * 60)
print("SIMULATING ANDROID BASE64 UPLOAD")
print("=" * 60)
import base64, io
from PIL import Image

# Read and compress like Android does (70% JPEG quality)
pil_img = Image.open(image_path).convert('RGB')
buf = io.BytesIO()
pil_img.save(buf, format='JPEG', quality=70)
b64 = base64.b64encode(buf.getvalue()).decode()
print("Base64 length:", len(b64))

# Decode back and save as temp file
decoded = base64.b64decode(b64)
temp_path = 'temp_android_sim.jpg'
with open(temp_path, 'wb') as f:
    f.write(decoded)

result2 = svc.predict(temp_path)
print("TOP LABEL after base64 round-trip:", result2['top_label'])
print("TOP CONFIDENCE after base64      :", result2['top_confidence'])
print()
if result2['top_confidence'] < 0.3:
    print("⚠️  CONFIRMED: Base64 compression is killing confidence")
    print("   Fix: increase Android JPEG quality from 70 to 95")
else:
    print("✅ Base64 encoding is fine — image model needs retraining")

os.remove(temp_path)
