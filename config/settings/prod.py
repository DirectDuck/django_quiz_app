from .base import *


DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
