from .base import *
import os

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {'timeout': 20}
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CORS_ALLOW_ALL_ORIGINS = True
CONFIDENCE_THRESHOLD = 0.30

# ── ML Model paths — built from BASE_DIR, no env vars ─────────────────────
_ML = os.path.join(BASE_DIR, 'autoaid', 'apps', 'ml_engine', 'models')

IMAGE_MODEL_PATH  = os.path.join(_ML, 'damage_classifier.h5')
AUDIO_MODEL_PATH  = os.path.join(_ML, 'audio_v4.keras')
TEXT_MODEL_PATH   = os.path.join(_ML, 'text_tfidf_model.pkl')
TEXT_LE_PATH      = os.path.join(_ML, 'text_label_encoder.pkl')
TEXT_CLASSES_PATH = os.path.join(_ML, 'text_classes.json')

# Force into environment so os.getenv() in predictor.py also finds them
os.environ['IMAGE_MODEL_PATH']  = IMAGE_MODEL_PATH
os.environ['AUDIO_MODEL_PATH']  = AUDIO_MODEL_PATH
os.environ['TEXT_MODEL_PATH']   = TEXT_MODEL_PATH
os.environ['TEXT_LE_PATH']      = TEXT_LE_PATH
os.environ['TEXT_CLASSES_PATH'] = TEXT_CLASSES_PATH