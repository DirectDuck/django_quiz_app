from .base import *


ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
