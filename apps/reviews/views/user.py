from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models as quizzes_models
from apps.reviews import verificators


@login_required
def quiz_submit_for_review_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    # Temporary disable
    # if not request.user.is_email_verified():
    #     messages.error(request, "You can't submit quiz with unverified e-mail.")
    #     return redirect("quizzes:detail", slug=quiz.slug)

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
def quiz_cancel_approved_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    suitable, message = verificators.is_quiz_suitable_for_approved_cancel(quiz)

    if not suitable:
        messages.error(request, message)
        return redirect("quizzes:detail", slug=quiz.slug)

    if request.POST:
        quiz.status = quizzes_models.Quiz.Status.DRAFT
        quiz.save()
        return redirect("quizzes:detail", slug=quiz.slug)

    context = {
        "quiz": quiz,
    }

    return TemplateResponse(request, "reviews/user/cancel_approved.html", context)
