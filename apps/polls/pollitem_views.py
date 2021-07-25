from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from . import models, forms


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
        # In this class happens all validation
        formset=forms.PollItemAnswerFormSet,
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
        poll_item_form = forms.PollItemForm(request.POST)
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
        poll_item_form = forms.PollItemForm()
        poll_item_answer_formset = PollItemAnswerFormset(instance=poll_item)

    context = {
        "poll": poll,
        "poll_item_form": poll_item_form,
        "poll_item_answer_formset": poll_item_answer_formset,
    }

    return TemplateResponse(request, "polls/item/create.html", context)


@login_required
def pollitem_edit_view(request, slug, index):
    poll = get_object_or_404(
        models.Poll.objects.all(),
        slug=slug,
    )

    if not (request.user.is_staff or request.user == poll.author):
        raise PermissionDenied

    # Getting PollItem
    poll_item = get_object_or_404(
        models.PollItem.objects.all(),
        poll__slug=slug,
        index=index,
    )

    # Creating formset for PollItemAnswer
    PollItemAnswerFormset = inlineformset_factory(
        models.PollItem,
        models.PollItemAnswer,
        # In this class happens all validation
        formset=forms.PollItemAnswerFormSet,
        fields=(
            "text",
            "correct",
        ),
        labels={"text": "Answer"},
        extra=0,
        min_num=models.PollItem.MIN_ANSWERS,
        max_num=models.PollItem.MAX_ANSWERS,
        can_delete=True,
    )

    if request.POST:
        # Loading form and formset with POST data
        poll_item_form = forms.PollItemForm(request.POST, instance=poll_item)
        poll_item_answer_formset = PollItemAnswerFormset(
            request.POST, instance=poll_item
        )

        if poll_item_form.is_valid():
            # Saving PollItem
            poll_item = poll_item_form.save()

            if poll_item_answer_formset.is_valid():
                # Saving formset
                poll_item_answer_formset.save()
                return redirect("polls:detail", slug=poll.slug)
    else:
        # Initializing form and formset with instances
        poll_item_form = forms.PollItemForm(instance=poll_item)
        poll_item_answer_formset = PollItemAnswerFormset(instance=poll_item)

    context = {
        "poll": poll,
        "poll_item": poll_item,
        "poll_item_form": poll_item_form,
        "poll_item_answer_formset": poll_item_answer_formset,
    }

    return TemplateResponse(request, "polls/item/edit.html", context)


@login_required
def pollitem_delete_view(request, slug, index):
    poll = get_object_or_404(
        models.Poll.objects.all(),
        slug=slug,
    )

    if not (request.user.is_staff or request.user == poll.author):
        raise PermissionDenied

    poll_item = get_object_or_404(
        models.PollItem.objects.all(),
        poll__slug=slug,
        index=index,
    )

    if request.POST:
        form = forms.PollItemDeleteForm(request.POST, instance=poll_item)

        if form.is_valid():
            poll_item.delete()
            return redirect("polls:detail", slug=poll.slug)
    else:
        form = forms.PollItemDeleteForm(instance=poll_item)

    context = {"poll": poll, "poll_item": poll_item, "form": form}

    return TemplateResponse(request, "polls/item/delete.html", context)
