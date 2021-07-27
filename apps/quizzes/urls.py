from django.urls import path

from .views import (
    quiz,
    quiz_item,
    quiz_result,
)


app_name = "quizzes"

urlpatterns = [
    # Quiz views
    # Since quiz's slugs have 4 random characters followed
    # by dash, there won't be any overlap with this urls
    path("list/", quiz.list_view, name="list"),
    path("create/", quiz.create_view, name="create"),
    path("<slug:slug>/", quiz.detail_view, name="detail"),
    path("<slug:slug>/edit/", quiz.edit_view, name="edit"),
    path("<slug:slug>/delete/", quiz.delete_view, name="delete"),
    # QuizItem views
    path(
        "<slug:slug>/item/create/",
        quiz_item.create_view,
        name="item_create",
    ),
    path(
        "<slug:slug>/item/<int:index>/",
        quiz_item.edit_view,
        name="item_edit",
    ),
    path(
        "<slug:slug>/item/<int:index>/delete/",
        quiz_item.delete_view,
        name="item_delete",
    ),
    # QuizResult views
    path(
        "<slug:slug>/results/",
        quiz_result.edit_view,
        name="results_edit",
    ),
]
