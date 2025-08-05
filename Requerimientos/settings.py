import os
import json
from pathlib import Path
import dj_database_url
from google.oauth2 import service_account

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'tu-secret-key-por-defecto-en-desarrollo')

DEBUG = True

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'codigos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

ROOT_URLCONF = 'Requerimientos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Requerimientos.wsgi.application'

# Base de datos
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')  # Aquí 'DATABASE_URL' es el nombre de la variable
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Almacenamiento S3
# settings.py — sección S3
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID        = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY    = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME  = os.environ.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_REGION_NAME       = 'us-east-2'

# Fuerza Signature v4
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Usa path-style URLs en vez de virtual-hosted
AWS_S3_ADDRESSING_STYLE  = 'path'

# Apunta al endpoint regional de path-style
AWS_S3_ENDPOINT_URL      = f'https://s3.{AWS_S3_REGION_NAME}.amazonaws.com'

AWS_QUERYSTRING_AUTH     = True
AWS_S3_FILE_OVERWRITE    = True
AWS_DEFAULT_ACL          = None


# Redirecciones de login/logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Usuario personalizado
AUTH_USER_MODEL = 'codigos.User'

# CSRF confiables
CSRF_TRUSTED_ORIGINS = ['https://instrumentos-iiesa.up.railway.app', 'http://localhost:8000']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
