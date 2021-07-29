from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from apps.quizzes import models, forms


@login_required
def list_view(request):
    quizzes = models.Quiz.objects.filter(author=request.user).order_by("-created")

    context = {
        "quizzes": quizzes,
    }

    return TemplateResponse(request, "quizzes/quiz/list.html", context)


@login_required
def create_view(request):

    if request.POST:
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("quizzes:detail", slug=instance.slug)
    else:
        form = forms.QuizForm()

    context = {
        "form": form,
    }

    return TemplateResponse(request, "quizzes/quiz/create.html", context)


@login_required
def detail_view(request, slug):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    quiz_items = quiz.items.order_by("index")

    context = {
        "quiz": quiz,
        "quiz_items": quiz_items,
    }

    return TemplateResponse(request, "quizzes/quiz/detail.html", context)


@login_required
def edit_view(request, slug):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    if request.POST:
        form = forms.QuizForm(request.POST, instance=quiz)

        if form.is_valid():
            instance = form.save()
            return redirect("quizzes:detail", slug=instance.slug)
    else:
        form = forms.QuizForm(instance=quiz)

    context = {"quiz": quiz, "form": form}

    return TemplateResponse(request, "quizzes/quiz/edit.html", context)


@login_required
def delete_view(request, slug):
    quiz = get_object_or_404(
        models.Quiz.objects.all(),
        slug=slug,
    )

    if not request.user == quiz.author:
        raise PermissionDenied

    if request.POST:
        form = forms.QuizDeleteForm(request.POST, instance=quiz)

        if form.is_valid():
            quiz.delete()
            return redirect("quizzes:list")
    else:
        form = forms.QuizDeleteForm(instance=quiz)

    context = {"quiz": quiz, "form": form}

    return TemplateResponse(request, "quizzes/quiz/delete.html", context)
