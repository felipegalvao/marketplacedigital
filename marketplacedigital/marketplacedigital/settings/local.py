# settings/local.py

from .base import *
from . import settings_secrets
from corsheaders.defaults import default_headers

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "marketplacedigital",
        "USER": settings_secrets.DB_USER,
        "PASSWORD": settings_secrets.DB_PASSWORD,
        "HOST": "localhost",
        "PORT": "",
    }
}

INSTALLED_APPS += ("debug_toolbar", )

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

SENDFILE_BACKEND = 'sendfile.backends.development'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'google.com',
    'localhost:8000',
    '127.0.0.1:8000',
    'https://sandbox.pagseguro.uol.com.br'
)

CORS_ALLOW_HEADERS = default_headers + (
    'access-control-allow-origin',
)

CORS_ALLOW_CREDENTIALS = True
