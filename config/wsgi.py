
import os
from django.core.wsgi import get_wsgi_application

# Use 'config.settings.production' in production, otherwise 'config.settings.dev'
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()