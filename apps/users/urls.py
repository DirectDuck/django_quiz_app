from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("profile/", views.user_profile_view, name="profile"),
    # E-mail verification temporarily disabled
    # path(
    #     "resend_verification_email/",
    #     views.resend_verification_email_view,
    #     name="resend_verification_email",
    # ),
]
