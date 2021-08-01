from django.urls import path

from . import views


app_name = "takes"

urlpatterns = [
    path("list/", views.quiz_explore_view, name="explore"),
    path("<slug:slug>/tryout/", views.quiz_tryout_view, name="tryout"),
    path(
        "<slug:slug>/tryout/results/",
        views.quiz_tryout_results_view,
        name="tryout_results",
    ),
]
