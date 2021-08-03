import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from allauth.account.admin import EmailAddress


class User(AbstractUser):
    """Main user model"""

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    # E-mail verification temporarily disabled

    # def is_email_verified(self):
    #     """Get email verification status"""

    #     return EmailAddress.objects.get(user=self).verified
