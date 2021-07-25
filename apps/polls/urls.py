from django.urls import path

from . import views


app_name = "polls"

urlpatterns = [
    # Since poll's slugs have 4 random characters followed
    # by dash, there won't be any overlap with this urls
    path("list/", views.poll_list_view, name="list"),
    path("create/", views.poll_create_view, name="create"),
    path("<slug:slug>/", views.poll_detail_view, name="detail"),
    path("<slug:slug>/edit/", views.poll_edit_view, name="edit"),
    path("<slug:slug>/delete/", views.poll_delete_view, name="delete"),
    path("<slug:slug>/item/create/", views.pollitem_create_view, name="item_create"),
    path("<slug:slug>/item/<int:index>/", views.pollitem_edit_view, name="item_edit"),
]
