
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parents[3]

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DEBUG', '0') == '1'

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'drf_spectacular',

    'autoaid.apps.users',
    'autoaid.apps.diagnostics',
    'autoaid.apps.ml_engine',
    'autoaid.apps.garages',
    'autoaid.apps.requests',
    'autoaid.apps.audit',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'autoaid.config.middleware.RequestIDMiddleware',
    'autoaid.apps.audit.middleware.AuditMiddleware',
]

ROOT_URLCONF = 'autoaid.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'autoaid.config.wsgi.application'
ASGI_APPLICATION = 'autoaid.config.asgi.application'

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///' + str(BASE_DIR / 'db.sqlite3'))

def parse_database_url(url: str):
    if url.startswith('postgres://') or url.startswith('postgresql://'):
        from urllib.parse import urlparse
        p = urlparse(url)
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': p.path.lstrip('/'),
            'USER': p.username,
            'PASSWORD': p.password,
            'HOST': p.hostname,
            'PORT': p.port or 5432,
        }
    if url.startswith('sqlite:///'):
        return {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': url.replace('sqlite:///', ''),
        }
    raise ValueError(f"Unsupported DATABASE_URL: {url}")

DATABASES = {'default': parse_database_url(DATABASE_URL)}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = os.getenv('MEDIA_URL', '/media/')
MEDIA_ROOT = os.getenv('MEDIA_ROOT', str(BASE_DIR / 'media'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

CORS_ALLOW_ALL_ORIGINS = True

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'autoaid.config.exceptions.custom_exception_handler',

    # Rate limiting
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': os.getenv('THROTTLE_USER', '300/day'),
        'anon': os.getenv('THROTTLE_ANON', '30/min'),
    },

    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'ALLOWED_VERSIONS': ('v1',),
    'DEFAULT_VERSION': 'v1',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'AutoAid API',
    'DESCRIPTION': 'AI Vehicle Diagnostics Backend',
    'VERSION': '1.0.0',
}

# JWT
JWT_ACCESS_LIFETIME_MIN = int(os.getenv('JWT_ACCESS_LIFETIME_MIN', '30'))
JWT_REFRESH_LIFETIME_DAYS = int(os.getenv('JWT_REFRESH_LIFETIME_DAYS', '7'))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=JWT_ACCESS_LIFETIME_MIN),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=JWT_REFRESH_LIFETIME_DAYS),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Upload limits
MAX_UPLOAD_MB = int(os.getenv('MAX_UPLOAD_MB', '50'))
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_MB * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# Celery
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

# Diagnostics confidence threshold
CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.75'))

# Webhooks
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')
WEBHOOK_TIMEOUT_SECONDS = int(os.getenv('WEBHOOK_TIMEOUT_SECONDS', '8'))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s] [%(request_id)s] %(message)s'
        },
    },
    'filters': {
        'request_id': {
            '()': 'autoaid.config.logging.RequestIDFilter'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['request_id'],
        }
    },
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}
