import os
import sys
import dj_database_url
import cloudinary # <--- CRÍTICO
import cloudinary.uploader
import cloudinary.api
from pathlib import Path

# ==========================================================
# 🛰️ ESCÁNER DE ENTORNO Y PARCHE TERMUX
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
# 🔑 SEGURIDAD Y ACCESO
# ==========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-otto-task-key-2026')
DEBUG = True 
ALLOWED_HOSTS = ['*', '.render.com']
CSRF_TRUSTED_ORIGINS = ['https://*.render.com', 'https://otto-market.onrender.com']

# ==========================================================
# 🧩 MÓDULOS DEL SISTEMA (APPS)
# ==========================================================
INSTALLED_APPS = [
    'cloudinary_storage', # DEBE ir antes de staticfiles
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
# 🗄️ BASE DE DATOS (NEON.TECH)
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
# 🛰️ CONEXIÓN MAESTRA CLOUDINARY (ANTI-BORRADO)
# ==========================================================
if not IS_TERMUX:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    
    # ESTO ES LO QUE TE FALTABA: INICIALIZAR LA LIBRERÍA MANUALMENTE
    cloudinary.config(
        cloud_name = "dmfhdilyd",
        api_key = "642517876794157",
        api_secret = "J2mI_u549p79q9KPr7mXqK6I8Yk",
        secure = True
    )
    
    CLOUDINARY_STORAGE = {
        'CLOUDINARY_URL': 'cloudinary://642517876794157:J2mI_u549p79q9KPr7mXqK6I8Yk@dmfhdilyd'
    }
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==========================================================
# 🔐 ALLAUTH & SOCIAL SETTINGS
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
SOCIALACCOUNT_LOGIN_ON_GET = True
