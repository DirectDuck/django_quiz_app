from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models as quizzes_models
from apps.reviews import verificators, forms, models, filters


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
        return redirect("reviews:detail", slug=quiz.slug)

    if request.POST:
        quiz.status = quizzes_models.Quiz.Status.REVIEW
        quiz.save()
        return redirect("reviews:detail", slug=quiz.slug)

    context = {
        "quiz": quiz,
    }

    return TemplateResponse(request, "reviews/staff/cancel_approved.html", context)


@login_required
def reviews_list_view(request):

    if not request.user.is_staff:
        raise PermissionDenied

    quizzes = (
        quizzes_models.Quiz.objects.exclude(status=quizzes_models.Quiz.Status.DRAFT)
        .order_by("-created")
        .prefetch_related("items")
        .annotate(completions=Count("completed_quizzes"))
    )

    current_sort_field = request.GET.get("sort_by")

    if current_sort_field:
        quizzes = quizzes.order_by(current_sort_field)

    quizzes = filters.QuizReviewFilter(request.GET, quizzes)

    filter_form = quizzes.form

    paginator = Paginator(quizzes.qs, 9)

    page = request.GET.get("page")

    try:
        quizzes = paginator.page(page)
    except PageNotAnInteger:
        quizzes = paginator.page(1)
    except EmptyPage:
        quizzes = paginator.page(paginator.num_pages)

    context = {
        "quizzes": quizzes,
        "filter_form": filter_form,
        "current_sort_field": current_sort_field,
    }

    return TemplateResponse(request, "reviews/staff/list.html", context)


@login_required
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

    return TemplateResponse(request, "reviews/staff/detail.html", context)


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
        quiz.save()
        return redirect("reviews:list")

    context = {
        "quiz": quiz,
    }

    return TemplateResponse(request, "reviews/staff/approve.html", context)


@login_required
def reviews_reject_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.filter(status=quizzes_models.Quiz.Status.REVIEW),
        slug=slug,
    )

    if not request.user.is_staff:
        raise PermissionDenied

    if request.POST:
        form = forms.QuizRejectedMessageForm(request.POST)

        if form.is_valid():
            models.QuizRejectedMessage.objects.filter(quiz=quiz).delete()
            instance = form.save(commit=False)
            instance.quiz = quiz
            instance.save()
            quiz.status = quizzes_models.Quiz.Status.REJECTED
            quiz.save()
            return redirect("reviews:list")

    else:
        form = forms.QuizRejectedMessageForm()

    context = {
        "quiz": quiz,
        "form": form,
    }

    return TemplateResponse(request, "reviews/staff/reject.html", context)


@login_required
def quiz_cancel_rejected_view(request, slug):
    quiz = get_object_or_404(
        quizzes_models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    suitable, message = verificators.is_quiz_suitable_for_rejected_cancel(quiz)

    if not suitable:
        messages.error(request, message)
        return redirect("reviews:detail", slug=quiz.slug)

    quiz.status = quizzes_models.Quiz.Status.REVIEW
    quiz.save()

    return redirect("reviews:detail", slug=quiz.slug)
