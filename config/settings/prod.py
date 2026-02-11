
from .base import *
import os

# --- MINIMAL SETTINGS FOR DEBUGGING ---

# Force DEBUG=True to see any errors
DEBUG = True

# Allow all hosts
ALLOWED_HOSTS = ['*']

# Use a temporary in-memory SQLite database.
# This avoids all file system and database connection issues.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Basic static files settings
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')

# Use the simplest possible storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# --- END MINIMAL SETTINGS ---