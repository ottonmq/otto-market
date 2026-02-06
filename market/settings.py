import os
import sys
import dj_database_url
from pathlib import Path
import cloudinary
import cloudinary.storage

# ==========================================================
# 🛰️ NÚCLEO DEL SISTEMA Y DETECCIÓN DE ENTORNO
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
IS_TERMUX = 'com.termux' in os.environ.get('PREFIX', '')

# --- PARCHE TERMUX (ERROR 38) ---
if IS_TERMUX:
    try:
        from django.core.files import locks
        locks.lock = lambda f, flags: True
        locks.unlock = lambda f: True
        
        import sqlite3
        from django.db.backends.sqlite3.base import DatabaseWrapper
        DatabaseWrapper.check_constraints = lambda self, connection=None: None
    except Exception:
        pass

# ==========================================================
# 🔑 SEGURIDAD NEÓN
# ==========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-otto-task-key-2026')
DEBUG = True 
ALLOWED_HOSTS = ['*', '.render.com']
CSRF_TRUSTED_ORIGINS = ['https://*.render.com', 'https://otto-market.onrender.com']

# ==========================================================
# 🧩 MÓDULOS DEL SISTEMA (APPS)
# ==========================================================
INSTALLED_APPS = [
    'cloudinary_storage',         # Captura de archivos en la nube
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

# 🚨 PUNTEROS DE CARPETA (market)
ROOT_URLCONF = 'market.urls'
WSGI_APPLICATION = 'market.wsgi.application'

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

# ==========================================================
# 🗄️ BASE DE DATOS: AUTO-DETECCIÓN INTELIGENTE
# ==========================================================
if not IS_TERMUX:
    # EN RENDER: POSTGRES OBLIGATORIO
    DATABASES = {
        'default': dj_database_url.config(
            default='postgresql://market_db_pnun_user:GakvaG9OoAiJxLdWrQaCtAFTrekH1DWJ@dpg-d61c049r0fns73fpu2ag-a.oregon-postgres.render.com/market_db_pnun',
            conn_max_age=600
        )
    }
else:
    # EN TERMUX: SQLITE LOCAL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==========================================================
# 🚀 ALMACENAMIENTO (STATIC & CLOUDINARY)
# ==========================================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# LÓGICA DE FOTOS PERSISTENTES
if not IS_TERMUX:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': 'dmfhdilyd',
        'API_KEY': '642517876794157',
        'API_SECRET': 'J2mI_u549p79q9KPr7mXqK6I8Yk'
    }
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==========================================================
# 🔐 PROTOCOLOS DE ACCESO (GOOGLE LOGIN)
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
