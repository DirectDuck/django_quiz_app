from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models, forms


@login_required
def quiz_item_view(request, slug, index):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not (request.user == quiz.author or request.user.is_staff):
        raise PermissionDenied

    quiz_item = get_object_or_404(
        models.QuizItem.objects.all(),
        quiz__slug=slug,
        index=index,
    )

    quiz_item_answers = quiz_item.answers.all()

    context = {
        "quiz": quiz,
        "quiz_item": quiz_item,
        "quiz_item_answers": quiz_item_answers,
    }

    return TemplateResponse(request, "quizzes/details_stricted/item.html", context)


@login_required
def quiz_results_view(request, slug):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not (request.user == quiz.author or request.user.is_staff):
        raise PermissionDenied

    quiz_results = models.QuizResult.objects.filter(quiz=quiz).order_by("score")

    context = {
        "quiz": quiz,
        "quiz_max_score": quiz.items.count(),
        "quiz_results": quiz_results,
    }

    return TemplateResponse(request, "quizzes/details_stricted/results.html", context)
