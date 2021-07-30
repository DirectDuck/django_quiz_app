from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models, forms


@login_required
def edit_view(request, slug):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    if quiz.status != models.Quiz.Status.DRAFT:
        raise PermissionDenied

    quiz.update_results()

    QuizResultFormSet = modelformset_factory(
        models.QuizResult,
        fields=("text",),
        labels={"text": "Result"},
        extra=0,
        can_delete=False,
        can_order=False,
    )

    if request.POST:
        quiz_result_formset = QuizResultFormSet(
            request.POST,
            queryset=quiz.results.all(),
        )

        if quiz_result_formset.is_valid():
            quiz_result_formset.save()
            return redirect("quizzes:detail", slug=quiz.slug)
    else:
        quiz_result_formset = QuizResultFormSet(
            queryset=quiz.results.all(),
        )

    context = {
        "quiz": quiz,
        "quiz_result_formset": quiz_result_formset,
        "quiz_max_score": quiz.items.count(),
    }

    return TemplateResponse(request, "quizzes/result/edit.html", context)
