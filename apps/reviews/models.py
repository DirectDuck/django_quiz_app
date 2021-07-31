from django.db import models

from apps.quizzes import models as quizzes_models


class QuizRejectedMessage(models.Model):
    """This model holds rejected message if quiz has been rejected"""

    quiz = models.OneToOneField(
        quizzes_models.Quiz, related_name="rejected_message", on_delete=models.CASCADE
    )

    text = models.CharField(max_length=255)
