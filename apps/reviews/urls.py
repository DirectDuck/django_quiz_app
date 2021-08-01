from django.urls import path

from .views import user, staff


app_name = "reviews"

urlpatterns = [
    # User views
    path("<slug:slug>/submit/", user.quiz_submit_for_review_view, name="submit"),
    path(
        "<slug:slug>/cancel_review/",
        user.quiz_cancel_review_view,
        name="cancel_review",
    ),
    path(
        "<slug:slug>/cancel_approve/",
        user.quiz_cancel_approved_view,
        name="user_cancel_approved",
    ),
    # Staff views
    path("list/", staff.reviews_list_view, name="list"),
    path("<slug:slug>/", staff.reviews_detail_view, name="detail"),
    path("<slug:slug>/approve/", staff.reviews_approve_view, name="approve"),
    path(
        "<slug:slug>/staff_cancel_approve/",
        staff.quiz_cancel_approved_view,
        name="staff_cancel_approved",
    ),
    path(
        "<slug:slug>/reject/",
        staff.reviews_reject_view,
        name="reject",
    ),
    path(
        "<slug:slug>/staff_cancel_reject/",
        staff.quiz_cancel_rejected_view,
        name="staff_cancel_reject",
    ),
]
