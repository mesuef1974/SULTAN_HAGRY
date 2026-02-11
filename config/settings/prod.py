from .base import *
import os

# --- PRODUCTION SETTINGS FOR RENDER ---

# إبقاء DEBUG مفعلاً مؤقتاً لسهولة التشخيص على Render (سنغلقه لاحقاً)
DEBUG = True

# السماح بكل المضيفين مؤقتاً
ALLOWED_HOSTS = ['*']

# استخدام قاعدة بيانات SQLite ملفية لضمان الاستقرار مؤقتاً على Render
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# إعدادات الملفات الثابتة مع WhiteNoise
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# إدراج WhiteNoise في الميدلوير إن لم يكن موجودًا
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# دعم البروكسي العكسي وإخراج السجلات إلى الكونسول
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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
}

# --- END RENDER SETTINGS ---