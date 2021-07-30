from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models as quizzes_models
from . import forms, models, verificators


def quiz_tryout_view(request, slug):
    quiz = get_object_or_404(quizzes_models.Quiz.objects.all(), slug=slug)

    if not (request.user.is_staff or request.user == quiz.author):
        raise PermissionDenied

    # Checking if quiz is suitable for tryout
    suitable, message = verificators.is_quiz_suitable_for_tryout(quiz)

    if not suitable:
        messages.error(request, message)
        return redirect("quizzes:detail", slug=quiz.slug)

    # Removing previous CompletedTryouts from this user/quiz pair
    models.CompletedTryout.remove_previous(request.user, quiz)

    # Getting number of quiz items (questions)
    quiz_items_count = quiz.items.count()

    # Creating formset from QuizItemTryoutForm
    QuizItemTryoutFormSet = formset_factory(
        forms.QuizItemTryoutForm,
        formset=forms.BaseQuizItemTryoutFormSet,
        # Setting number of forms to be equal to number of questions
        extra=quiz_items_count,
    )

    if request.POST:
        # Filling formset with POST data and list of quiz items
        quiz_item_tryout_formset = QuizItemTryoutFormSet(
            request.POST,
            form_kwargs={
                "quiz_item_list": list(
                    quiz.items.order_by("index").prefetch_related("answers")
                ),
            },
        )

        if quiz_item_tryout_formset.is_valid():
            # Creating CompletedTryout object
            completed_tryout = models.CompletedTryout.objects.create(
                user=request.user, quiz=quiz, score=0
            )

            # Creating related to CompletedTryout CompletedTryoutAnswer
            # objects from form data
            completed_tryout_answers = []
            for form in quiz_item_tryout_formset:
                completed_tryout_answers.append(
                    models.CompletedTryoutAnswer.initialize_from_answer_pk(
                        completed_tryout,
                        int(form.cleaned_data["answers"]),
                    )
                )

            models.CompletedTryoutAnswer.objects.bulk_create(completed_tryout_answers)

            # Updating CompletedTryout score to match number of correct answers
            # from related CompletedTryoutAnswer
            completed_tryout.update_score()

            return redirect("takes:tryout_results", slug=quiz.slug)
    else:
        # Just in case you are wondering: form_kwargs argument
        # will be interceipt in BaseQuizItemTryoutFormSet method
        # and there we will get quiz_item from quiz_item_list,
        # that is required to build the form itself.
        # There are many ways you can achieve that behavior, but
        # this one gives the performance I am satisfied with.
        # Kudos to datalowe
        # https://forum.djangoproject.com/t/pass-different-parameters-to-each-form-in-formset/4040/2
        quiz_item_tryout_formset = QuizItemTryoutFormSet(
            form_kwargs={
                "quiz_item_list": list(
                    quiz.items.order_by("index").prefetch_related("answers")
                ),
            }
        )

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
