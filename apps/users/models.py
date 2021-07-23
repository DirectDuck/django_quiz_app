from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
