from django.urls import path, include

from apps.quizzes.api import views as quizzes_views

app_name = "api"

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/signup/", include("dj_rest_auth.registration.urls")),
    path("quiz/", quizzes_views.QuizApiView.as_view(), name="quiz_list"),
]
