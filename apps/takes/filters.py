import django_filters

from apps.quizzes import models as quizzes_models


class QuizExploreFilter(django_filters.FilterSet):

    o = django_filters.OrderingFilter(
        fields=(("created", "created"),),
        empty_label="No ordering",
        label="",
        widget=django_filters.widgets.LinkWidget,
    )

    class Meta:
        model = quizzes_models.Quiz
        fields = tuple()
