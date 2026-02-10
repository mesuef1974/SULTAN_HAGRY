import pytest
import django
from django.conf import settings

def test_pytest_setup():
    """Verify that pytest is working correctly."""
    assert True

def test_django_version():
    """Verify that Django version is accessible."""
    assert django.get_version() != ""
