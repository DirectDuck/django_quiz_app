import django_filters

from apps.quizzes import models as quizzes_models


class QuizReviewFilter(django_filters.FilterSet):

    status = django_filters.ChoiceFilter(
        # To prevent filtering DRAFT quizzes
        choices=quizzes_models.Quiz.Status.choices[1:],
        empty_label="All",
        label="",
    )

    class Meta:
        model = quizzes_models.Quiz
        fields = ("status",)
