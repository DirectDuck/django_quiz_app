from django.urls import path, include

from apps.takes.api import views as takes_views

app_name = "api"

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/signup/", include("dj_rest_auth.registration.urls")),
    path("explore/", takes_views.ExploreApiView.as_view(), name="explore"),
    path("take/<slug:slug>/", takes_views.QuizTakeApiView.as_view(), name="take"),
    path("results/", takes_views.QuizTakeResultsApiView.as_view(), name="results"),
]
