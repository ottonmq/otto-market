import os
import dj_database_url
from pathlib import Path

# --- 1. RUTAS BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 2. SEGURIDAD ---
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-otto-task-key-2026')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*', '.render.com'] 
CSRF_TRUSTED_ORIGINS = ['https://*.render.com']

# --- 3. APPS (ORDEN MAESTRO PARA QUE EL ADMIN SE VEA BIEN) ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Siempre antes de Cloudinary para el Admin
    
    # Almacenamiento
    'cloudinary_storage',
    'cloudinary',
    
    # Sistema
    'django.contrib.sites',
    'marketapp',
    
    # Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# --- 4. MIDDLEWARE (ORDEN CRÍTICO PARA EL DISEÑO) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ESTO ARREGLA EL DISEÑO DEL ADMIN
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

# --- 6. BASE DE DATOS ---
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600
    )
}

# --- 7. ESTÁTICOS Y MEDIA (BLINDAJE RENDER) ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Forzamos a WhiteNoise para el Admin y Cloudinary para tus fotos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- 8. ALLAUTH & DEFAULTS ---
SITE_ID = 1
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', 'allauth.account.auth_backends.AuthenticationBackend']
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SOCIALACCOUNT_LOGIN_ON_GET = True
