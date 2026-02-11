
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls.i18n import i18n_patterns # Disabled for debugging
from django.conf.urls.static import static

# URLs that should not be translated
urlpatterns = [
    # path('i18n/', include('django.conf.urls.i18n')), # Disabled
    path('admin/', admin.site.urls),
    # path('health/', include('health_check.urls')), # Disabled until apps are re-enabled
    # path('api/memory/', include('project_memory.urls')), # Disabled until apps are re-enabled
    
    # Adding coredata urls directly without i18n
    path('', include('coredata.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)