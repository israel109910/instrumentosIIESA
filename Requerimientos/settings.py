from pathlib import Path
import os
import dj_database_url

# =============================
# Configuración base del proyecto
# =============================

BASE_DIR = Path(__file__).resolve().parent.parent

# =============================
# Seguridad
# =============================

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', '+bh4@(y1sbv2c#+1p179=$fgj-oht55g0k3o!0c0wo#hz#y%&q')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'  # Cambia en producción

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

# =============================
# Aplicaciones instaladas
# =============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',  # Para AWS S3
    'codigos',
]

# =============================
# Middleware
# =============================

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

# =============================
# URLS y WSGI
# =============================

ROOT_URLCONF = 'Requerimientos.urls'
WSGI_APPLICATION = 'Requerimientos.wsgi.application'

# =============================
# Templates
# =============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Asegúrate de tener esta carpeta
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

# =============================
# Base de datos
# =============================

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# =============================
# Validación de contraseñas
# =============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================
# Internacionalización
# =============================

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# =============================
# Archivos estáticos
# =============================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================
# Almacenamiento en S3
# =============================

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID        = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY    = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME  = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME       = 'us-east-2'

AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_ADDRESSING_STYLE  = 'path'
AWS_S3_ENDPOINT_URL      = f'https://s3.{AWS_S3_REGION_NAME}.amazonaws.com'

AWS_QUERYSTRING_AUTH     = False  # True si quieres URLs firmadas (privadas)
AWS_S3_FILE_OVERWRITE    = False
AWS_DEFAULT_ACL          = None

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# =============================
# Usuario personalizado
# =============================

AUTH_USER_MODEL = 'codigos.User'

# =============================
# Redirecciones de login/logout
# =============================

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# =============================
# CSRF Trusted Origins (Railway)
# =============================

CSRF_TRUSTED_ORIGINS = [
    'https://instrumentos-iiesa.up.railway.app',
    'http://localhost:8000',
]

# =============================
# Configuración general
# =============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
