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
