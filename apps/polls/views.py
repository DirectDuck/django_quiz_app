from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from . import models, forms


@login_required
def poll_list_view(request):
    polls = models.Poll.objects.filter(author=request.user).order_by("-created")

    context = {
        "polls": polls,
    }

    return TemplateResponse(request, "polls/list.html", context)


@login_required
def poll_create_view(request):

    if request.POST:
        form = forms.PollCreateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect("pages:home")
    else:
        form = forms.PollCreateForm()

    context = {
        "form": form,
    }

    return TemplateResponse(request, "polls/create.html", context)


@login_required
def poll_detail_view(request, slug):
    poll = get_object_or_404(
        models.Poll.objects.all(),
        slug=slug,
    )

    if not (request.user.is_staff or request.user == poll.author):
        raise PermissionDenied

    context = {
        "poll": poll,
    }

    return TemplateResponse(request, "polls/detail.html", context)


@login_required
def poll_edit_view(request, slug):
    poll = get_object_or_404(
        models.Poll.objects.all(),
        slug=slug,
    )

    if not (request.user.is_staff or request.user == poll.author):
        raise PermissionDenied

    if request.POST:
        form = forms.PollEditForm(request.POST, instance=poll)

        if form.is_valid():
            instance = form.save()
            return redirect("polls:detail", slug=instance.slug)
    else:
        form = forms.PollEditForm(instance=poll)

    context = {"poll": poll, "form": form}

    return TemplateResponse(request, "polls/edit.html", context)


@login_required
def poll_delete_view(request, slug):
    poll = get_object_or_404(
        models.Poll.objects.all(),
        slug=slug,
    )

    if not (request.user.is_staff or request.user == poll.author):
        raise PermissionDenied

    if request.POST:
        form = forms.PollDeleteForm(request.POST, instance=poll)

        if form.is_valid():
            poll.delete()
            return redirect("polls:list")
    else:
        form = forms.PollDeleteForm(instance=poll)

    context = {"poll": poll, "form": form}

    return TemplateResponse(request, "polls/delete.html", context)
