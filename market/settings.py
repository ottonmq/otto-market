import os
import sys
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

# ==========================================================
# 🛰️ ESCÁNER DE ENTORNO Y PARCHE TERMUX (ERROR 38)
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
IS_TERMUX = 'com.termux' in os.environ.get('PREFIX', '')

if IS_TERMUX:
    try:
        from django.core.files import locks
        locks.lock = lambda f, flags: True
        locks.unlock = lambda f: True
    except Exception:
        pass

# ==========================================================
# 🔑 SEGURIDAD Y ACCESO (CYBERPUNK SHIELD)
# ==========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-otto-task-key-2026')
DEBUG = True 
ALLOWED_HOSTS = ['*', '.render.com']
CSRF_TRUSTED_ORIGINS = ['https://*.render.com', 'https://otto-market.onrender.com']

# ==========================================================
# 🧩 MÓDULOS DEL SISTEMA (APPS) - EL ORDEN ES VITAL
# ==========================================================
INSTALLED_APPS = [
    'cloudinary_storage', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',          
    'django.contrib.sites',
    'marketapp',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
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
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'market.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'market.wsgi.application'

# ==========================================================
# 🗄️ BASE DE DATOS (NEON.TECH / SQLITE FALLBACK)
# ==========================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600
    )
}

# ==========================================================
# 🚀 ALMACENAMIENTO ESTÁTICO (WHITENOISE)
# ==========================================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# ==========================================================
# 🛰️ CONEXIÓN MAESTRA CLOUDINARY (SOPORTE AR ACTIVADO)
# ==========================================================
if not IS_TERMUX:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': 'dmfhdilyd',
        'API_KEY': '223926243589726',
        'API_SECRET': '5J3GsVsYrr8ecpXoJKdBD-LpaQ4',
        'RESOURCE_TYPES': ['image', 'video', 'raw'], # ⚡ PERMITE .GLB PARA AR
    }

    cloudinary.config(
        cloud_name = "dmfhdilyd",
        api_key = "223926243589726",
        api_secret = "5J3GsVsYrr8ecpXoJKdBD-LpaQ4",
        secure = True
    )
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==========================================================
# 🔐 CONFIGURACIÓN DE CUENTAS (ALLAUTH)
# ==========================================================
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# FINAL DEL ARCHIVO - SOLICITUD DE DMFHDILYD
SOCIALACCOUNT_LOGIN_ON_GET = True

# ==========================================================
# 🤖 NÚCLEO SHADOW (GEMINI AI CONFIG) & TELEGRAM
# ==========================================================
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') 
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
# ESTO ES LO QUE PIDE EL HACKATHON:
AUTH0_AUDIENCE = f"https://{AUTH0_DOMAIN}/api/v2/"



