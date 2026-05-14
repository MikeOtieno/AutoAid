import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'autoaid.config.settings.development'
django.setup()
from django.conf import settings

print('IMAGE :', settings.IMAGE_MODEL_PATH)
print('IMAGE EXISTS:', os.path.exists(str(settings.IMAGE_MODEL_PATH or '')))
print('AUDIO :', settings.AUDIO_MODEL_PATH)
print('AUDIO EXISTS:', os.path.exists(str(settings.AUDIO_MODEL_PATH or '')))
print('TEXT  :', settings.TEXT_MODEL_PATH)
print('TEXT  EXISTS:', os.path.exists(str(settings.TEXT_MODEL_PATH or '')))
print('THRESHOLD   :', settings.CONFIDENCE_THRESHOLD)
