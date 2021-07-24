from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from allauth.account.admin import EmailAddress

from .models import User


@login_required
def user_profile_view(request):
    email_verified = EmailAddress.objects.get(user=request.user).verified

    if not email_verified:
        messages.add_message(
            request,
            messages.WARNING,
            mark_safe(
                "Your e-mail is not verified. "
                f'<a href={reverse("users:resend_verification_email")}>'
                "Resend verification e-mail.</a>"
            ),
        )

    context = {}

    return TemplateResponse(request, "users/profile.html", context)


@login_required
def resend_verification_email_view(request):
    user_email = EmailAddress.objects.get(user=request.user)
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
