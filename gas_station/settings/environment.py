import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')

ROOT_URLCONF = 'gas_station.urls'

WSGI_APPLICATION = 'gas_station.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'