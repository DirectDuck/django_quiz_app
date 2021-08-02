import django_heroku

from .base import *


ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

django_heroku.settings(locals())
