
from pathlib import Path
import environ
import os
from django.utils.translation import gettext_lazy as _

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read .env file only if it exists
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY', default='dev-secret-key-change-me')

DEBUG = True
ALLOWED_HOSTS = ['*']

# --- MINIMAL INSTALLED APPS ---
INSTALLED_APPS = [
    # 'jazzmin', # Disabled for debugging
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps - ALL DISABLED
    # 'rest_framework',
    # 'django_htmx',
    # 'tailwind',
    # 'theme',
    # 'rangefilter',
    # 'import_export',
    # 'health_check',
    # 'health_check.db',
    # 'health_check.cache',
    # 'health_check.storage',
    # 'simple_history',

    # Local apps - ALL DISABLED
    # 'coredata',
    # 'project_memory',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'simple_history.middleware.HistoryRequestMiddleware', # Disabled
    # 'django_htmx.middleware.HtmxMiddleware', # Disabled
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database is handled in prod.py

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'