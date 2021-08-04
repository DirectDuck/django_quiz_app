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


# Security

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True


# Django-admin two-factor auth

INSTALLED_APPS += ["django_otp", "django_otp.plugins.otp_totp"]

MIDDLEWARE += ["django_otp.middleware.OTPMiddleware"]


# Sentry

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
