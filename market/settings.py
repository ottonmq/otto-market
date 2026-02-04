import os
import dj_database_url
from pathlib import Path

# --- 1. RUTAS BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 2. SEGURIDAD ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-otto-task-premium-key-2026')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# IMPORTANTE: Para Render y el Bot
ALLOWED_HOSTS = ['*', '.render.com'] 
CSRF_TRUSTED_ORIGINS = ['https://*.render.com'] # Evita errores 403 en el Bot

# --- 3. APPS (SISTEMA + CLOUDINARY + MARKET) ---
INSTALLED_APPS = [
    'cloudinary_storage', # Siempre antes de staticfiles
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Cloudinary Core
    'cloudinary',
    
    # Módulos de visibilidad y red
    'django.contrib.sites',
    'django.contrib.sitemaps',
    
    # Tu App de mercado (Asegúrate que el nombre sea correcto)
    'marketapp',
    
    # Autenticación Cyberpunk (Allauth)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
]

# --- 4. MIDDLEWARE (ORDEN CRÍTICO PARA WHITENOISE) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Para que Render sirva el CSS/JS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'market.urls'

# --- 5. PLANTILLAS ---
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
                'django.template.context_processors.media', 
                'marketapp.context_processors.contadores_globales',
            ],
        },
    },
]

WSGI_APPLICATION = 'market.wsgi.application'

# --- 6. BASE DE DATOS (HÍBRIDA) ---
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600
    )
}

# --- 7. INTERNACIONALIZACIÓN ---
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- 8. STATIC & MEDIA (OPTIMIZADO PARA CLOUDINARY) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Almacenamiento Dual: Estáticos en WhiteNoise, Media en Cloudinary
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- 9. CONFIGURACIÓN ALLAUTH & SITES ---
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True 
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
LOGIN_REDIRECT_URL = 'perfil'
LOGOUT_REDIRECT_URL = 'home'
ACCOUNT_EMAIL_VERIFICATION = "none"

# --- 10. DEFAULTS ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
