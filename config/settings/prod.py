from .base import *


DEBUG = False

ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")


# Database config

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": "",
    }
}


# Email

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_USER = env("EMAIL_SMTP_USER")
EMAIL_HOST = env("EMAIL_SMTP_HOST")
EMAIL_PORT = env("EMAIL_SMTP_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = env("EMAIL_SMTP_PASSWORD")


# Sentry

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
