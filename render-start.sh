#!/bin/bash

# Exit on error
set -o errexit

echo "==> Running Migrations..."
# First, try to migrate normally
python manage.py migrate --noinput || {
    echo "==> Standard migration failed, attempting to fix migration graph..."
    # If it fails due to NodeNotFoundError, we might need to fake some nodes 
    # but usually, just having the apps in INSTALLED_APPS fixes it.
    # We will try a second time after ensuring apps are loaded.
    python manage.py migrate --noinput
}

echo "==> Creating Superuser..."
python manage.py initadmin

echo "==> Collecting Static Files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn..."
export DJANGO_SETTINGS_MODULE=config.settings.prod
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000