from django.urls import path

from . import poll_views, pollitem_views


app_name = "polls"

urlpatterns = [
    # Since poll's slugs have 4 random characters followed
    # by dash, there won't be any overlap with this urls
    # Poll views
    path("list/", poll_views.poll_list_view, name="list"),
    path("create/", poll_views.poll_create_view, name="create"),
    path("<slug:slug>/", poll_views.poll_detail_view, name="detail"),
    path("<slug:slug>/edit/", poll_views.poll_edit_view, name="edit"),
    path("<slug:slug>/delete/", poll_views.poll_delete_view, name="delete"),
    # PollItem views
    path(
        "<slug:slug>/item/create/",
        pollitem_views.pollitem_create_view,
        name="item_create",
    ),
    path(
        "<slug:slug>/item/<int:index>/",
        pollitem_views.pollitem_edit_view,
        name="item_edit",
    ),
    path(
        "<slug:slug>/item/<int:index>/delete/",
        pollitem_views.pollitem_delete_view,
        name="item_delete",
    ),
]
