from django.urls import path

from . import views


app_name = "polls"

urlpatterns = [
    path("list/", views.poll_list_view, name="list"),
    path("create/", views.poll_create_view, name="create"),
]
