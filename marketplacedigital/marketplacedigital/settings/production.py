# settings/production.py

from .base import *

DEBUG = False

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = settings_secrets.EMAIL_HOST
EMAIL_HOST_USER = settings_secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = settings_secrets.EMAIL_HOST_PASSWORD
EMAIL_PORT = settings_secrets.EMAIL_PORT
EMAIL_USE_TLS = settings_secrets.EMAIL_USE_TLS

# Replace DB settings to use PostgreSQL on Heroku
import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS += ("felipegalvao.pythonanywhere.com", )

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "felipegalvao$marketplacedigital",
        "USER": settings_secrets.PRODUCTION_DB_USER,
        "PASSWORD": settings_secrets.PRODUCTION_DB_PASSWORD,
        "HOST": "felipegalvao.mysql.pythonanywhere-services.com",
        "PORT": "",
    }
}

BASE_DOMAIN = 'http://felipegalvao.pythonanywhere.com/'
