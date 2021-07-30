from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models, forms


@login_required
def quiz_item_details_stricted_view(request, slug, index):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    if quiz.status != models.Quiz.Status.DRAFT:
        raise PermissionDenied

    # Getting QuizItem
    quiz_item = get_object_or_404(
        models.QuizItem.objects.all(),
        quiz__slug=slug,
        index=index,
    )

    context = {
        "quiz": quiz,
        "quiz_item": quiz_item,
        "quiz_item_form": quiz_item_form,
        "quiz_item_answer_formset": quiz_item_answer_formset,
    }

    return TemplateResponse(request, "quizzes/item/edit.html", context)


@login_required
def quiz_resulsts_details_stricted_view(request, slug):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    if quiz.status != models.Quiz.Status.DRAFT:
        raise PermissionDenied

    context = {
        "quiz": quiz,
        "quiz_max_score": quiz.items.count(),
    }

    return TemplateResponse(request, "quizzes/result/edit.html", context)
