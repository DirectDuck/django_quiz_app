from .base import *


ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
