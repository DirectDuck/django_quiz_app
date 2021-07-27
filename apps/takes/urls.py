from django.urls import path

from . import views


app_name = "takes"

urlpatterns = [
    path("<slug:slug>/tryout/", views.quiz_tryout_view, name="tryout"),
]
