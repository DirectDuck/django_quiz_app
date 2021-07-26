from django.urls import path

from . import quiz_views, quizitem_views


app_name = "quizzes"

urlpatterns = [
    # Quiz views
    # Since quiz's slugs have 4 random characters followed
    # by dash, there won't be any overlap with this urls
    path("list/", quiz_views.quiz_list_view, name="list"),
    path("create/", quiz_views.quiz_create_view, name="create"),
    path("<slug:slug>/", quiz_views.quiz_detail_view, name="detail"),
    path("<slug:slug>/edit/", quiz_views.quiz_edit_view, name="edit"),
    path("<slug:slug>/delete/", quiz_views.quiz_delete_view, name="delete"),
    # QuizItem views
    path(
        "<slug:slug>/item/create/",
        quizitem_views.quizitem_create_view,
        name="item_create",
    ),
    path(
        "<slug:slug>/item/<int:index>/",
        quizitem_views.quizitem_edit_view,
        name="item_edit",
    ),
    path(
        "<slug:slug>/item/<int:index>/delete/",
        quizitem_views.quizitem_delete_view,
        name="item_delete",
    ),
]
