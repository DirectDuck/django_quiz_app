import django_filters

from apps.quizzes import models


class QuizListFilter(django_filters.FilterSet):

    status = django_filters.ChoiceFilter(
        choices=models.Quiz.Status.choices,
        empty_label="All",
        label="",
    )

    class Meta:
        model = models.Quiz
        fields = ("status",)
