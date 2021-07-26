from unidecode import unidecode

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string


class Quiz(models.Model):
    """Model representing quizzes"""

    class Status(models.IntegerChoices):
        DRAFT = 1  # When initially created
        WAITING_FOR_REVIEW = 2  # When author finishes quiz creation
        REJECTED = 3  # If admin/editor reject quiz (comes with RejectedQuizMessage)
        APPROVED = 4  # If admin/editor approves quiz (approved quiz will be published)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quizzes"
    )

    title = models.CharField(max_length=65)
    slug = models.SlugField(max_length=130, unique=True)

    description = models.TextField(max_length=255)

    # If True, other users will see the quiz
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

        while Quiz.objects.filter(slug=slug).exists():
            slug = get_random_string(length=4) + "-" + slugified_title

        self.slug = slug
        super().save(*args, **kwargs)

    def get_status_badge_type(self):
        """Get bootstrap color representation based on
        quiz status"""

        if self.status == Quiz.Status.DRAFT:
            return "secondary"
        elif self.status == Quiz.Status.WAITING_FOR_REVIEW:
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

        index = 1

        while self.items.filter(index=index).exists():
            index += 1

        return index

    def update_items_indexes(self):
        """Update quiz items indexes in case there might
        be any inconsistency"""
        index = 1
        for item in self.items.order_by("index"):
            item.index = index
            item.save()


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
        constraints = [
            # All questions in quiz must be unique
            models.UniqueConstraint(
                fields=["quiz", "question"], name="unique_quiz_questions"
            ),
            # Every item must have it's own unique index
            models.UniqueConstraint(fields=["quiz", "index"], name="unique_quiz_index"),
        ]

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

    class Meta:
        # How can you guess the correct answer if there
        # is multiple identical answers?
        constraints = [
            models.UniqueConstraint(
                fields=["quiz_item", "text"], name="unique_quizitem_text"
            ),
        ]

    def __str__(self):
        return f"{self.quiz_item}'s answer"


class QuizResult:
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

    class Meta:
        # There can't be two different result messages for one score
        constraints = [
            models.UniqueConstraint(fields=["quiz", "score"], name="unique_quiz_score"),
        ]
