from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Django
    path("admin/", admin.site.urls),
    # 3rd-party
    path("", include("allauth.urls")),
    # Local
    path("", include("apps.pages.urls", namespace="pages")),
]
