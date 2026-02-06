import os
import sys
import dj_database_url
from pathlib import Path
import cloudinary
import cloudinary.storage

# ==========================================================
# 🛰️ NÚCLEO DEL SISTEMA
# ==========================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# 🔑 SEGURIDAD NEÓN
# ==========================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-otto-task-key-2026')
DEBUG = True 
ALLOWED_HOSTS = ['*', '.render.com']
CSRF_TRUSTED_ORIGINS = ['https://*.render.com', 'https://otto-market.onrender.com']

# ==========================================================
# 🧩 MÓDULOS DEL SISTEMA (ORDEN DE PRIORIDAD)
# ==========================================================
INSTALLED_APPS = [
    'cloudinary_storage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',
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
# 🗄️ BASE DE DATOS: INYECCIÓN DIRECTA (SOLUCIÓN AL ERROR)
# ==========================================================
# Extraemos los datos de la URL para que no haya fallos de ENGINE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'market_db_pnun',
        'USER': 'market_db_pnun_user',
        'PASSWORD': 'GakvaG9OoAiJxLdWrQaCtAFTrekH1DWJ',
        'HOST': 'dpg-d61c049r0fns73fpu2ag-a.oregon-postgres.render.com',
        'PORT': '5432',
    }
}

# ==========================================================
# 🚀 ALMACENAMIENTO: CLOUDINARY TOTAL
# ==========================================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dmfhdilyd',
    'API_KEY': '642517876794157',
    'API_SECRET': 'J2mI_u549p79q9KPr7mXqK6I8Yk'
}

cloudinary.config(
    cloud_name = 'dmfhdilyd',
    api_key = '642517876794157',
    api_secret = 'J2mI_u549p79q9KPr7mXqK6I8Yk',
    secure = True
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==========================================================
# 🔐 PROTOCOLOS DE ACCESO
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
