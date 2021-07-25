from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from . import models, forms


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
