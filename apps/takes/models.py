from django.db import models
from django.conf import settings

from apps.quizzes.models import Quiz, QuizItemAnswer


class CompletedTryout(models.Model):
    """Model containing information about tryout completed by user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="completed_tryout",
        on_delete=models.CASCADE,
    )

    quiz = models.ForeignKey(
        Quiz,
        related_name="completed_tryout",
        on_delete=models.CASCADE,
    )

    score = models.PositiveIntegerField()


class CompletedTryoutAnswer(models.Model):
    """Model to store user answers for tryout"""

    completed_tryout = models.ForeignKey(
        CompletedTryout,
        related_name="answers",
        on_delete=models.CASCADE,
    )

    item_answer = models.ForeignKey(
        QuizItemAnswer,
        on_delete=models.CASCADE,
    )
