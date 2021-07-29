from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from allauth.account.admin import EmailAddress

from .models import User


@login_required
def user_profile_view(request):
    try:
        email_verified = EmailAddress.objects.get(user=request.user).verified
    except EmailAddress.DoesNotExist:
        # Creating e-mail object in case user was not created
        # via allauth
        email_verified = EmailAddress.objects.create(
            user=request.user,
            email=request.user.email,
        ).verified

    # Added second condition here, so if user actually resends
    # his verification e-mail, only one message will appear
    if not email_verified and len(messages.get_messages(request)) == 0:
        messages.add_message(
            request,
            messages.WARNING,
            "Your e-mail is not verified. "
            f'<a href={reverse("users:resend_verification_email")}>'
            "Resend verification e-mail.</a>",
        )

    context = {}

    return TemplateResponse(request, "users/profile.html", context)


@login_required
def resend_verification_email_view(request):
    try:
        user_email = EmailAddress.objects.get(user=request.user)
    except:
        # Creating e-mail object in case user was not created
        # via allauth
        user_email = EmailAddress.objects.create(
            user=request.user,
            email=request.user.email,
        )

    if not user_email.verified:
        user_email.send_confirmation(request)
        messages.add_message(
            request,
            messages.INFO,
            f"E-mail verification sent to {user_email.email}",
        )
    else:
        messages.add_message(
            request,
            messages.INFO,
            "Your e-mail address already verified",
        )

    return redirect("users:profile")
