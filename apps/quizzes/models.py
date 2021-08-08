from unidecode import unidecode

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string


class Quiz(models.Model):
    """Model representing quizzes"""

    MIN_ITEMS_COUNT = 3
    MAX_ITEMS_COUNT = 15

    class Status(models.IntegerChoices):
        DRAFT = 1  # When initially created
        REVIEW = 2  # When author finishes quiz creation and staff reviews the work
        REJECTED = 3  # If admin/editor reject quiz (comes with RejectedQuizMessage)
        APPROVED = 4  # If admin/editor approves quiz (approved quiz is visible in explore page)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes"
    )

    title = models.CharField(max_length=65)
    slug = models.SlugField(max_length=130, unique=True)

    description = models.TextField(max_length=255)

    status = models.IntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generating unique slug
        if not self.slug:
            slugified_title = slugify(unidecode(self.title))[:30]
            slug = get_random_string(length=4) + "-" + slugified_title

            while Quiz.objects.filter(slug=slug).exists():
                slug = get_random_string(length=4) + "-" + slugified_title

            self.slug = slug
        super().save(*args, **kwargs)

    def get_status_badge_type(self):
        """Get bootstrap color representation based on
        quiz status"""

        if self.status == Quiz.Status.DRAFT:
            return "secondary"
        elif self.status == Quiz.Status.REVIEW:
            return "info"
        elif self.status == Quiz.Status.REJECTED:
            return "danger"
        elif self.status == Quiz.Status.APPROVED:
            return "success"

        raise NotImplementedError(
            "Did you forgot to update get_status_badge_type method?"
        )

    def get_available_item_index(self):
        """Get free index based on quiz items presented"""

        if self.items.all().exists():
            index = self.items.order_by("-index")[0].index + 1
        else:
            index = 1

        return index

    def update_items_indexes(self):
        """Update quiz items indexes in case there might
        be any inconsistency"""

        index = 1

        items = []

        for item in self.items.order_by("index"):
            item.index = index
            items.append(item)
            index += 1

        self.items.bulk_update(items, ["index"])

    def update_results(self) -> None:
        """Create/update/delete related QuizResult objects
        to match the number of items"""

        # If everything is up to date, then number of items
        # should be 1 less than number of results (because they include
        # zero)

        items_count = self.items.count()
        results_count = self.results.count()

        if items_count + 1 > results_count:
            for i in range(results_count, items_count + 1):
                self.results.get_or_create(
                    quiz=self,
                    score=i,
                )
        elif items_count + 1 < results_count:
            for result in self.results.filter(score__gt=items_count):
                result.delete()

    def is_completed_by(self, user):
        """Check if user completed this quiz"""
        return self.completed_quizzes.filter(user=user).exists()


class QuizItem(models.Model):
    """Model representing container for single question-answers item
    in quiz"""

    MIN_ANSWERS = 2
    MAX_ANSWERS = 6
    MIN_CORRECT_ANSWERS = 1
    MAX_CORRECT_ANSWERS = 1

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="items",
    )

    question = models.CharField(max_length=65)

    index = models.PositiveIntegerField()

    class Meta:
        ordering = ["index"]

    def __str__(self):
        return f"{self.quiz.title} - {self.index} item"


class QuizItemAnswer(models.Model):
    """Model representing single answer in quizzes item"""

    quiz_item = models.ForeignKey(
        QuizItem,
        on_delete=models.CASCADE,
        related_name="answers",
    )

    text = models.CharField(max_length=65)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quiz_item}'s answer"


class QuizResult(models.Model):
    """Model representing different results of particular quiz,
    based on the number of correct answers by user"""

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="results",
    )

    score = models.PositiveIntegerField()

    text = models.CharField(
        max_length=65,
        # Because QuizResult will be initialized automatically
        blank=True,
    )
