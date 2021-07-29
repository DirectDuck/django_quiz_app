from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models, forms


@login_required
def create_view(request, slug):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    # Initializing empty QuizItem
    quiz_item = models.QuizItem()

    # Creating formset for QuizItemAnswer
    QuizItemAnswerFormset = inlineformset_factory(
        models.QuizItem,
        models.QuizItemAnswer,
        # In this class happens all validation
        formset=forms.QuizItemAnswerFormSet,
        fields=(
            "text",
            "correct",
        ),
        labels={"text": "Answer"},
        extra=0,
        min_num=models.QuizItem.MIN_ANSWERS,
        max_num=models.QuizItem.MAX_ANSWERS,
    )

    if request.POST:
        # Loading form and formset with POST data
        # We actually need to put POST in formset here
        # in case QuizItem form validation fails,
        # otherwise we would have lost formset data
        quiz_item_form = forms.QuizItemForm(request.POST, quiz=quiz)
        quiz_item_answer_formset = QuizItemAnswerFormset(
            request.POST, instance=quiz_item
        )

        if quiz_item_form.is_valid():
            # Saving QuizItem and assigning some data
            quiz_item = quiz_item_form.save(commit=False)
            quiz_item.index = quiz.get_available_item_index()
            quiz_item.quiz = quiz

            # Reinitializing QuizItemAnswer formset so it
            # can use newly created QuizItem instead of
            # empty one we created initially
            quiz_item_answer_formset = QuizItemAnswerFormset(
                request.POST, instance=quiz_item
            )

            if quiz_item_answer_formset.is_valid():
                # Saving everything we have
                quiz_item.save()
                quiz_item_answer_formset.save()
                return redirect("quizzes:detail", slug=quiz.slug)
    else:
        # Initializing basically empty form and formset
        quiz_item_form = forms.QuizItemForm(quiz=quiz)
        quiz_item_answer_formset = QuizItemAnswerFormset(instance=quiz_item)

    context = {
        "quiz": quiz,
        "quiz_item_form": quiz_item_form,
        "quiz_item_answer_formset": quiz_item_answer_formset,
    }

    return TemplateResponse(request, "quizzes/item/create.html", context)


@login_required
def edit_view(request, slug, index):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    # Getting QuizItem
    quiz_item = get_object_or_404(
        models.QuizItem.objects.all(),
        quiz__slug=slug,
        index=index,
    )

    # Creating formset for QuizItemAnswer
    QuizItemAnswerFormset = inlineformset_factory(
        models.QuizItem,
        models.QuizItemAnswer,
        # In this class happens all validation
        formset=forms.QuizItemAnswerFormSet,
        fields=(
            "text",
            "correct",
        ),
        labels={"text": "Answer"},
        extra=0,
        min_num=models.QuizItem.MIN_ANSWERS,
        max_num=models.QuizItem.MAX_ANSWERS,
        can_delete=True,
    )

    if request.POST:
        # Loading form and formset with POST data
        quiz_item_form = forms.QuizItemForm(request.POST, instance=quiz_item, quiz=quiz)
        quiz_item_answer_formset = QuizItemAnswerFormset(
            request.POST, instance=quiz_item
        )

        if quiz_item_form.is_valid():
            # Saving QuizItem
            quiz_item = quiz_item_form.save()

            if quiz_item_answer_formset.is_valid():
                # Saving formset
                quiz_item_answer_formset.save()
                return redirect("quizzes:detail", slug=quiz.slug)
    else:
        # Initializing form and formset with instances
        quiz_item_form = forms.QuizItemForm(instance=quiz_item, quiz=quiz)
        quiz_item_answer_formset = QuizItemAnswerFormset(instance=quiz_item)

    context = {
        "quiz": quiz,
        "quiz_item": quiz_item,
        "quiz_item_form": quiz_item_form,
        "quiz_item_answer_formset": quiz_item_answer_formset,
    }

    return TemplateResponse(request, "quizzes/item/edit.html", context)


@login_required
def delete_view(request, slug, index):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    quiz_item = get_object_or_404(
        models.QuizItem.objects.all(),
        quiz__slug=slug,
        index=index,
    )

    if request.POST:
        form = forms.QuizItemDeleteForm(request.POST, instance=quiz_item)

        if form.is_valid():
            quiz_item.delete()
            quiz.update_items_indexes()
            return redirect("quizzes:detail", slug=quiz.slug)
    else:
        form = forms.QuizItemDeleteForm(instance=quiz_item)

    context = {"quiz": quiz, "quiz_item": quiz_item, "form": form}

    return TemplateResponse(request, "quizzes/item/delete.html", context)
