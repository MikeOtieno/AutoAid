import sys, os

sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'autoaid.config.settings.development'

import django
django.setup()

from django.conf import settings
from autoaid.apps.ml_engine.services.audio_infer import AudioInferenceService
from autoaid.apps.ml_engine.services.predictor import Predictor

# ── Test audio model in isolation ─────────────────────────────────────────────
print("=" * 60)
print("AUDIO MODEL ISOLATION TEST")
print("=" * 60)

svc = AudioInferenceService(settings.AUDIO_MODEL_PATH)
result = svc.predict(
    r'C:\Users\mikeo\Desktop\car_damage_detection\dead_battery\dead_battery_1.wav'
)
print("TOP LABEL     :", result['top_label'])
print("TOP CONFIDENCE:", result['top_confidence'])
print("TOP 3         :")
for item in result['explanation']['top3']:
    print(f"   {item['confidence']:.2%}  {item['label']}")

# ── Test full predictor fusion ────────────────────────────────────────────────
print()
print("=" * 60)
print("FULL PREDICTOR FUSION TEST")
print("=" * 60)

predictor = Predictor()
fused = predictor.predict(
    image_path=None,
    audio_path=r'C:\Users\mikeo\Desktop\car_damage_detection\dead_battery\dead_battery_1.wav',
    text='my car won t start I hear a clicking sound dead battery',
)
print("DIAGNOSIS     :", fused['diagnosis'])
print("CONFIDENCE    :", fused['confidence'])
print("RECOMMENDED   :", fused['recommended_action'])
print()
print("FUSION DETAIL :")
for e in fused['explanation']['fusion']['evidence']:
    print(f"   [{e['source']}] {e['label']} — {e['confidence']:.2%}")
print("SCORES        :", fused['explanation']['fusion']['scores'])
