
import os
from django.core.wsgi import get_wsgi_application
import django.utils.html

# --- Monkey Patch for Jazzmin + Django 5.x/6.x compatibility ---
# We keep this because it's necessary for the admin theme
original_format_html = django.utils.html.format_html

def patched_format_html(format_string, *args, **kwargs):
    if not args and not kwargs:
        return format_string
    return original_format_html(format_string, *args, **kwargs)

django.utils.html.format_html = patched_format_html
# ---------------------------------------------------------------

# Use 'config.settings.prod' in production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

# Get the application
application = get_wsgi_application()

# Vercel expects 'app' variable
app = application