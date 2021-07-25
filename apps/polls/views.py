from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from . import models, forms, formsets


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


@login_required
def pollitem_create_view(request, slug):
    poll = get_object_or_404(
        models.Poll.objects.all(),
        slug=slug,
    )

    if not (request.user.is_staff or request.user == poll.author):
        raise PermissionDenied

    # Initializing empty PollItem
    poll_item = models.PollItem()

    # Creating formset for PollItemAnswer
    PollItemAnswerFormset = inlineformset_factory(
        models.PollItem,
        models.PollItemAnswer,
        formset=formsets.PollItemAnswerFormSet,
        fields=(
            "text",
            "correct",
        ),
        labels={"text": "Answer"},
        extra=0,
        min_num=models.PollItem.MIN_ANSWERS,
        max_num=models.PollItem.MAX_ANSWERS,
    )

    if request.POST:
        # Loading form and formset with POST data
        # We actually need to put POST in formset here
        # in case PollItem form validation fails,
        # otherwise we would have lost formset data
        poll_item_form = forms.PollItemCreateForm(request.POST)
        poll_item_answer_formset = PollItemAnswerFormset(
            request.POST, instance=poll_item
        )

        if poll_item_form.is_valid():
            # Saving PollItem and assigning some data
            poll_item = poll_item_form.save(commit=False)
            poll_item.index = poll.get_available_index()
            poll_item.poll = poll

            # Reinitializing PollItemAnswer formset so it
            # can use newly created PollItem instead of
            # empty one we created initially
            poll_item_answer_formset = PollItemAnswerFormset(
                request.POST, instance=poll_item
            )

            if poll_item_answer_formset.is_valid():
                # Saving everything we have
                poll_item.save()
                poll_item_answer_formset.save()
                return redirect("polls:detail", slug=poll.slug)
    else:
        # Initializing basically empty form and formset
        poll_item_form = forms.PollItemCreateForm()
        poll_item_answer_formset = PollItemAnswerFormset(instance=poll_item)

    context = {
        "poll": poll,
        "poll_item_form": poll_item_form,
        "poll_item_answer_formset": poll_item_answer_formset,
    }

    return TemplateResponse(request, "polls/item_create.html", context)
