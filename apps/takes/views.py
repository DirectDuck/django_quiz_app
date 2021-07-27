from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models as quizzes_models
from . import forms, models


def quiz_tryout_view(request, slug):
    quiz = get_object_or_404(quizzes_models.Quiz.objects.all(), slug=slug)

    if not (request.user.is_staff or request.user == quiz.author):
        raise PermissionDenied

    models.CompletedTryout.remove_previous(request.user, quiz)

    quiz_items_count = quiz.items.count()

    QuizItemTryoutFormSet = formset_factory(
        forms.QuizItemTryoutForm,
        formset=forms.BaseQuizItemTryoutFormSet,
        extra=quiz_items_count,
    )

    if request.POST:
        quiz_item_tryout_formset = QuizItemTryoutFormSet(
            request.POST,
            form_kwargs={"quiz": quiz},
        )
        if quiz_item_tryout_formset.is_valid():
            completed_tryout = models.CompletedTryout.objects.create(
                user=request.user, quiz=quiz, score=0
            )
            for form in quiz_item_tryout_formset:
                models.CompletedTryoutAnswer.create_from_answer_pk(
                    completed_tryout,
                    int(form.cleaned_data["answers"]),
                )

            completed_tryout.update_score()

            return redirect("takes:tryout_results", slug=quiz.slug)
    else:
        quiz_item_tryout_formset = QuizItemTryoutFormSet(form_kwargs={"quiz": quiz})

    context = {
        "quiz": quiz,
        "quiz_items_count": quiz_items_count,
        "quiz_item_tryout_formset": quiz_item_tryout_formset,
    }

    return TemplateResponse(request, "takes/tryout.html", context)


@login_required
def quiz_tryout_results_view(request, slug):
    quiz = get_object_or_404(quizzes_models.Quiz.objects.all(), slug=slug)

    completed_tryout = get_object_or_404(
        models.CompletedTryout.objects.all(), user=request.user, quiz=quiz
    )

    if not (request.user.is_staff or request.user == quiz.author):
        raise PermissionDenied

    quiz_items_count = quiz.items.count()

    context = {
        "quiz": quiz,
        "quiz_items_count": quiz_items_count,
        "completed_tryout": completed_tryout,
    }

    return TemplateResponse(request, "takes/tryout_results.html", context)
