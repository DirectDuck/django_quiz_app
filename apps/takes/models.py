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

    def update_score(self):
        """Update score based on number of correct answers
        in related CompletedTryoutAnswer objects"""

        self.score = self.answers.filter(item_answer__correct=True).count()
        self.save(update_fields=["score"])

    def get_result_message(self):
        """Get result text from QuizResult based on current score"""

        quiz_result = self.quiz.results.filter(score=self.score)

        if not quiz_result.exists():
            raise Exception(
                "Something went wrong!"
                "Are you sure you didn't modified quiz while trying it out?"
            )

        return quiz_result.first().text

    @classmethod
    def remove_previous(cls, user, quiz):
        """Remove previous CompletedTryout instances for given user/quiz pair"""

        cls.objects.filter(user=user, quiz=quiz).delete()


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

    @classmethod
    def initialize_from_answer_pk(cls, completed_tryout, item_answer_pk):
        """Get initialized (but not created in db)
        CompletedTryoutAnswer from CompletedTryout and QuizItemAnswer's pk"""

        item_answer = QuizItemAnswer.objects.get(pk=item_answer_pk)

        return cls(
            completed_tryout=completed_tryout,
            item_answer=item_answer,
        )


class CompletedQuiz(models.Model):
    """Model containing information about quiz completed by user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="completed_quizzes",
        on_delete=models.CASCADE,
    )

    quiz = models.ForeignKey(
        Quiz,
        related_name="completed_quizzes",
        on_delete=models.CASCADE,
    )

    score = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def update_score(self):
        """Update score based on number of correct answers
        in related CompletedQuizAnswer objects"""

        self.score = self.answers.filter(item_answer__correct=True).count()
        self.save(update_fields=["score"])

    def get_result_message(self):
        """Get result text from QuizResult based on current score"""

        quiz_result = self.quiz.results.filter(score=self.score)

        if not quiz_result.exists():
            raise Exception("Something went wrong!")

        return quiz_result.first().text

    @classmethod
    def remove_previous(cls, user, quiz):
        """Remove previous CompletedTryout instances for given user/quiz pair"""

        cls.objects.filter(user=user, quiz=quiz).delete()


class CompletedQuizAnswer(models.Model):
    """Model to store user answers for tryout"""

    completed_quiz = models.ForeignKey(
        CompletedQuiz,
        related_name="answers",
        on_delete=models.CASCADE,
    )

    item_answer = models.ForeignKey(
        QuizItemAnswer,
        on_delete=models.CASCADE,
    )

    @classmethod
    def initialize_from_answer_pk(cls, completed_quiz, item_answer_pk):
        """Get initialized (but not created in db)
        CompletedQuizAnswer from CompletedTryout and QuizItemAnswer's pk"""

        item_answer = QuizItemAnswer.objects.get(pk=item_answer_pk)

        return cls(
            completed_quiz=completed_quiz,
            item_answer=item_answer,
        )
