from pathlib import Path
import os
import dj_database_url

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = '+bh4@(y1sbv2c#+1p179=$fgj-oht55g0k3o!0c0wo#hz#y%&q'
DEBUG = True
 # Cambia a False en producción

ALLOWED_HOSTS = ['*', 'instrumentosiiesa-production.up.railway.app', 'localhost']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',  # Para django-storages y S3
    'codigos',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Sirve archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

# URL raíz de la app
ROOT_URLCONF = 'Requerimientos.urls'

# Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

#{
 #   'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
   # }
#}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Idioma y zona horaria
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos multimedia
# Aunque en S3 no usas MEDIA_ROOT ni MEDIA_URL localmente, puedes dejarlo así para pruebas locales
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Redirecciones
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# Usuario personalizado
AUTH_USER_MODEL = 'codigos.User'

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


# CSRF para Railway
CSRF_TRUSTED_ORIGINS = [
    'https://instrumentos-iiesa.up.railway.app',
    'http://localhost:8000'
]

# Campo por defecto para modelos nuevos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'