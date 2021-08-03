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
