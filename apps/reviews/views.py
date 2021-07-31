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
        quiz.published = False
        quiz.save()
        return redirect("quizzes:detail", slug=quiz.slug)

    context = {
        "quiz": quiz,
    }

    return TemplateResponse(request, "reviews/cancel_approved.html", context)


def quiz_staff_cancel_approved_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    suitable, message = verificators.is_quiz_suitable_for_approved_cancel(quiz)

    if not suitable:
        messages.error(request, message)
        return redirect("reviews:detail", slug=quiz.slug)

    if request.POST:
        quiz.status = quizzes_models.Quiz.Status.REVIEW
        quiz.published = False
        quiz.save()
        return redirect("reviews:detail", slug=quiz.slug)

    context = {
        "quiz": quiz,
    }

    return TemplateResponse(request, "reviews/staff_cancel_approved.html", context)


@login_required
def reviews_list_view(request):

    if not request.user.is_staff:
        raise PermissionDenied

    quizzes = (
        quizzes_models.Quiz.objects.exclude(status=quizzes_models.Quiz.Status.DRAFT)
        .order_by("-created")
        .prefetch_related("items")
    )

    context = {
        "quizzes": quizzes,
    }

    return TemplateResponse(request, "reviews/list.html", context)


def reviews_detail_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.exclude(status=quizzes_models.Quiz.Status.DRAFT),
        slug=slug,
    )

    if not request.user.is_staff:
        raise PermissionDenied

    quiz_items = quiz.items.order_by("index")

    context = {
        "quiz": quiz,
        "quiz_items": quiz_items,
    }

    return TemplateResponse(request, "reviews/detail.html", context)


@login_required
def reviews_approve_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.filter(status=quizzes_models.Quiz.Status.REVIEW),
        slug=slug,
    )

    if not request.user.is_staff:
        raise PermissionDenied

    if request.POST:
        quiz.status = quizzes_models.Quiz.Status.APPROVED
        quiz.published = True
        quiz.save()
        return redirect("reviews:list")

    context = {
        "quiz": quiz,
    }

    return TemplateResponse(request, "reviews/approve.html", context)


@login_required
def reviews_reject_view(request, slug):
    pass
