
import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

# Get the WSGI application
application = get_wsgi_application()

# Vercel needs 'app' variable
app = application