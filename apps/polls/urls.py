from django.urls import path

from . import views


app_name = "polls"

urlpatterns = [
    path("create/", views.poll_create_view, name="create"),
]
