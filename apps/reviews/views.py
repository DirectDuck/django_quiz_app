from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models as quizzes_models

from . import verificators


@login_required
def quiz_submit_for_review_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    if not request.user.is_email_verified():
        messages.error(request, "You can't submit quiz with unverified e-mail.")
        return redirect("quizzes:detail", slug=quiz.slug)

    suitable, message = verificators.is_quiz_suitable_for_submission(quiz)

    if not suitable:
        messages.error(request, message)
        return redirect("quizzes:detail", slug=quiz.slug)

    quiz.status = quiz.Status.REVIEW
    quiz.save()

    messages.success(request, message)

    return redirect("quizzes:detail", slug=quiz.slug)


@login_required
def quiz_cancel_review_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    suitable, message = verificators.is_quiz_suitable_for_review_cancel(quiz)

    if not suitable:
        messages.error(request, message)
        return redirect("quizzes:detail", slug=quiz.slug)

    quiz.status = quiz.Status.DRAFT
    quiz.save()

    messages.success(request, message)

    return redirect("quizzes:detail", slug=quiz.slug)


@login_required
def reviews_list_view(request):

    if not request.user.is_staff:
        raise PermissionDenied

    quizzes = (
        quizzes_models.Quiz.objects.filter(status=quizzes_models.Quiz.Status.REVIEW)
        .order_by("-created")
        .prefetch_related("items")
    )

    context = {
        "quizzes": quizzes,
    }

    return TemplateResponse(request, "reviews/list.html", context)
