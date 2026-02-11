
from django.apps import AppConfig

# Renaming this app to coredata
class CoredataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coredata'