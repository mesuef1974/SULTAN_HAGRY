
from .base import *
import os
import dj_database_url

# FORCE DEBUG to be False in production, but allow override for troubleshooting
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# Allow all hosts for Vercel deployment
ALLOWED_HOSTS = ['*']

# Security settings
# Vercel handles SSL termination, so we need to trust the headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Disable SSL Redirect to avoid infinite loops behind Vercel proxy
SECURE_SSL_REDIRECT = False 

# WhiteNoise configuration for static files
try:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ValueError:
    pass # Middleware might already be there

# Vercel specific static files configuration
# In Vercel, we should not try to create directories at runtime.
# The build process should handle collectstatic.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Use simpler storage that doesn't require manifest generation (safer for Vercel)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files on Vercel (Read-only fallback)
# Vercel doesn't support persistent local storage. 
# For production, consider using AWS S3, Cloudinary, or Azure Storage.
# We redirect MEDIA_ROOT to /tmp just to avoid startup crashes if something tries to write.
MEDIA_ROOT = '/tmp/media'

# Database configuration
# Check if DATABASE_URL is set
if os.environ.get('DATABASE_URL'):
    try:
        # Simplified database config for maximum compatibility
        db_config = dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
        DATABASES = {
            'default': db_config
        }
    except Exception as e:
        print(f"Error configuring database: {e}")
        # Fallback to SQLite if DB config fails (so the app at least starts)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
else:
    print("WARNING: DATABASE_URL not found, using SQLite")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Logging configuration to see errors in Vercel logs
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
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}