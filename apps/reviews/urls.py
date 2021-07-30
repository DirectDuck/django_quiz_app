from django.urls import path

from . import views


app_name = "reviews"

urlpatterns = [
    path("<slug:slug>/submit/", views.quiz_submit_for_review_view, name="submit"),
    path(
        "<slug:slug>/cancel_review/",
        views.quiz_cancel_review_view,
        name="cancel_review",
    ),
    path("list/", views.reviews_list_view, name="list"),
    path("<slug:slug>", views.reviews_detail_view, name="detail"),
    path("<slug:slug>/approve/", views.reviews_approve_view, name="approve"),
]
