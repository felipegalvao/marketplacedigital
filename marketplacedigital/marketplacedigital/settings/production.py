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

ALLOWED_HOSTS += ("www.linkplace.com.br", )

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

# Database setting
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

# Current Base Domain setting
BASE_DOMAIN = 'http://felipegalvao.pythonanywhere.com/'

# Amazon AWS settings for S3 storage
DEFAULT_FILE_STORAGE = 'marketplacedigital.settings.s3utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'marketplacedigital.settings.s3utils.StaticRootS3BotoStorage'

AWS_ACCESS_KEY_ID = settings_secrets.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings_secrets.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = settings_secrets.AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

SENDFILE_BACKEND = 'sendfile.backends.mod_wsgi'

PAGSEGURO_BASE_URL = 'https://ws.sandbox.pagseguro.uol.com.br/'
