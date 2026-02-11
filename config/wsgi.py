
import os
import django.utils.html
from django.core.wsgi import get_wsgi_application

# --- Monkey Patch for Jazzmin + Django 5.x/6.x compatibility ---
# Fixes: TypeError: args or kwargs must be provided in format_html
original_format_html = django.utils.html.format_html

def patched_format_html(format_string, *args, **kwargs):
    if not args and not kwargs:
        return format_string
    return original_format_html(format_string, *args, **kwargs)

django.utils.html.format_html = patched_format_html
# ---------------------------------------------------------------

# Use 'config.settings.production' in production, otherwise 'config.settings.dev'
settings_module = os.environ.get('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
app = application