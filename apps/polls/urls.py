from django.urls import path

from . import views


app_name = "polls"

urlpatterns = [
    path("list/", views.poll_list_view, name="list"),
    path("create/", views.poll_create_view, name="create"),
    path("detail/<slug:slug>/", views.poll_detail_view, name="detail"),
    path("edit/<slug:slug>/", views.poll_edit_view, name="edit"),
    path("delete/<slug:slug>/", views.poll_delete_view, name="delete"),
]
