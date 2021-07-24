from django.conf import settings
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

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
