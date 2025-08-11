# main/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-fxs2hr41*4fzex3a3g_rcm2k-c@5u_e_zs9097pck^a9qio6pr'
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # ajuste no deploy

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservas',
    'usuarios',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # ADICIONE templates/ na raiz do projeto
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # injeta variáveis úteis em todos os templates
                'main.context_processors.settings_extras',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

DATABASES = {
    # Você pode manter SQLite para o front. A API DRF está em outro serviço (MySQL).
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Localização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # crie a pasta
STATIC_ROOT = BASE_DIR / 'staticfiles'    # para collectstatic em produção

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Config da API (ajuste para o seu backend real)
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8001')  # Ex.: porta da API DRF
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))

# Endpoints default (parametrizáveis via env)
API_ENDPOINTS = {
    'jwt_obtain': os.getenv('API_JWT_OBTAIN', '/api/token/'),  # ou '/auth/jwt/create/' (Djoser)
    'campos': os.getenv('API_CAMPOS', '/api/campos/'),
    'campo_detail': os.getenv('API_CAMPO_DETAIL', '/api/campos/{id}/'),
    'disponibilidade': os.getenv('API_DISPONIBILIDADE', '/api/campos/{id}/disponibilidade/'),
    'reservas': os.getenv('API_RESERVAS', '/api/reservas/'),
}