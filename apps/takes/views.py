from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models as quizzes_models
from . import forms


def quiz_tryout_view(request, slug):
    quiz = get_object_or_404(quizzes_models.Quiz.objects.all(), slug=slug)

    if not (request.user.is_staff or request.user == quiz.author):
        raise PermissionDenied

    # TODO: alidation of availability of quiz to be tried out

    quiz_items_count = quiz.items.count()

    QuizItemTryoutFormSet = formset_factory(
        forms.QuizItemTryoutForm,
        formset=forms.BaseQuizItemTryoutFormSet,
        extra=quiz_items_count,
    )

    if request.POST:
        print(request.POST)
        quiz_item_tryout_formset = QuizItemTryoutFormSet(
            request.POST,
            form_kwargs={"quiz": quiz},
        )
    else:
        quiz_item_tryout_formset = QuizItemTryoutFormSet(form_kwargs={"quiz": quiz})

    context = {
        "quiz": quiz,
        "quiz_items_count": quiz_items_count,
        "quiz_item_tryout_formset": quiz_item_tryout_formset,
    }

    return TemplateResponse(request, "takes/tryout.html", context)
