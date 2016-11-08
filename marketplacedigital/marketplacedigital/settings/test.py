from .base import *
from . import settings_secrets
import autoslug

BASE_DOMAIN = 'http://localhost:8000/'



MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.fields.AutoSlugField': lambda: None
}