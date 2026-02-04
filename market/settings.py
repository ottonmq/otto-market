import os
import dj_database_url
from pathlib import Path

# --- 1. RUTAS BASE ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 2. SEGURIDAD ---
SECRET_KEY = 'django-insecure-wskp$fl8&frfe3=uk^ue+$5*(*sjpvmd#5f!2ac$k@y1g@r1q0'
DEBUG = False  # MODO PRODUCCIÓN ACTIVADO
ALLOWED_HOSTS = ['*']

# --- 3. APPS (SISTEMA + OTTO-MARKET) ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # AYUDA A WHITENOISE EN DESARROLLO
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Tu App
    'marketapp',
    
    # Autenticación Cyberpunk (Allauth)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
]

# --- 4. MIDDLEWARE (ORDEN CRÍTICO) ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- INYECTADO AQUÍ PARA ESTÁTICOS
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

# --- 6. BASE DE DATOS (CONEXIÓN AUTOMÁTICA RENDER) ---
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# --- 7. INTERNACIONALIZACIÓN ---
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- 8. STATIC & MEDIA ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ALMACENAMIENTO DE ESTÁTICOS PARA PRODUCCIÓN
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- 9. CONFIGURACIÓN MAESTRA ALLAUTH ---
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Flujo de entrada directa sin pantallas blancas
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True 
SOCIALACCOUNT_ADAPTER = 'allauth.socialaccount.adapter.DefaultSocialAccountAdapter'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_VERIFICATION = "none"

# Autenticación moderna
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Redirecciones
LOGIN_REDIRECT_URL = 'perfil'
LOGOUT_REDIRECT_URL = 'home'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

# --- 10. PARCHES Y DEFAULT FIELDS ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# PARCHE PARA LOCKS EN SISTEMAS MÓVILES/TERMUX
try:
    from django.core.files import locks
    locks.lock = lambda f, flags: True
    locks.unlock = lambda f: True
except (ImportError, AttributeError):
    pass

FILE_UPLOAD_PERMISSIONS = 0o644
