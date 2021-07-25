from unidecode import unidecode

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string


class Poll(models.Model):
    """Model representing polls"""

    class Status(models.IntegerChoices):
        DRAFT = 1  # When initially created
        WAITING_FOR_REVIEW = 2  # When author finishes poll creation
        REJECTED = 3  # If admin/editor reject poll (comes with RejectedPollMessage)
        APPROVED = 4  # If admin/editor approves poll (approved poll will be published)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="polls"
    )

    title = models.CharField(max_length=65)
    slug = models.SlugField(max_length=130, unique=True)

    # If True, other users will see the poll
    published = models.BooleanField(default=False)

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generating unique slug
        slugified_title = slugify(unidecode(self.title))
        slug = get_random_string(length=4) + "-" + slugified_title

        while Poll.objects.filter(slug=slug).exists():
            slug = get_random_string(length=4) + "-" + slugified_title

        self.slug = slug
        super().save(*args, **kwargs)
