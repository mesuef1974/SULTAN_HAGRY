
from django.http import HttpResponse
from django.urls import path

# --- DEBUGGING STEP ---
# This is a temporary, minimal URL configuration to isolate the startup crash.
# It bypasses all other apps, models, and views.

def health_check_view(request):
    return HttpResponse("Minimal URL is working. The crash is in the original urls.py or an included app.", status=200)

urlpatterns = [
    path('', health_check_view),
    # We are intentionally not including admin, i18n, or any other app's URLs for now.
]