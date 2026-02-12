
from .base import *
import os
import dj_database_url

# --- PRODUCTION SETTINGS ---

# 1. Security
DEBUG = False # Never run with debug on in production
SECRET_KEY = os.environ.get('SECRET_KEY') # Must be set in Vercel env vars

ALLOWED_HOSTS = ['*'] # Vercel handles routing, but ideally list specific domains

# 2. Database (PostgreSQL)
# We use dj_database_url to parse the DATABASE_URL env var
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=True,
    )
}

# 3. Static Files (WhiteNoise)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 4. Media Files
# Vercel filesystem is ephemeral. We need external storage (S3/Cloudinary).
# For now, we warn that local media will be lost.
MEDIA_ROOT = '/tmp/media' 

# 5. Security Headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# 6. Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO', # Log info and above in production
    },
}