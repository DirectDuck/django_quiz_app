from django.urls import path

from . import views


app_name = "takes"

urlpatterns = [
    path("explore/", views.quiz_explore_view, name="explore"),
    path("tryout/<slug:slug>/", views.quiz_tryout_view, name="tryout"),
    path(
        "tryout/<slug:slug>/results/",
        views.quiz_tryout_results_view,
        name="tryout_results",
    ),
    path("take/<slug:slug>/", views.quiz_take_view, name="take"),
    path(
        "take/<slug:slug>/results/",
        views.quiz_take_results_view,
        name="take_results",
    ),
]
