from django.db import models
from django.conf import settings
from django.utils import timezone
import hashlib
import base64
import os
import uuid
import io
from PIL import Image
from django.core.files.base import ContentFile
from cryptography.fernet import Fernet
from django.contrib.auth.models import Group

# --- LAZY KEY LOADING ---
def get_fernet():
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

class EncryptedCharField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None: return value
        try:
            f = get_fernet()
            return f.decrypt(value.encode()).decode()
        except: return value

    def get_prep_value(self, value):
        if value is None: return value
        try:
            f = get_fernet()
            return f.encrypt(value.encode()).decode()
        except: return value

# --- PROXY MODELS TO AVOID CLASHES ---
# We use existing tables from coredata but allow diagnostics to reference them
class DiagnosticStaff(models.Model):
    class Meta:
        managed = False
        db_table = 'coredata_staff'
        app_label = 'diagnostics'

def get_evidence_upload_path(instance, filename):
    # This is a stub to satisfy old migrations if they reference it
    from coredata.models import get_evidence_upload_path as real_path
    return real_path(instance, filename)