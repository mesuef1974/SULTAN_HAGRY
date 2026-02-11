from .base import *
import os
import dj_database_url

# --- PRODUCTION SETTINGS FOR RENDER (PostgreSQL) ---

# Turn off DEBUG for production once verified
DEBUG = True 

# Set a proper SECRET_KEY from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Use the hostname provided by Render
ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME', '*')]

# Database configuration: Use DATABASE_URL from Render (PostgreSQL)
# Fallback to local SQLite if DATABASE_URL is not set
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600
    )
}

# Static files configuration with WhiteNoise
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Ensure WhiteNoise is in Middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Logging configuration to see errors in Render Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Security settings for production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# --- END RENDER SETTINGS ---