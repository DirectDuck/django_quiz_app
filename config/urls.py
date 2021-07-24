from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found


# Disable unused urls from 3rd party libraries
disabled_urls = [
    path("email/", page_not_found, kwargs={"exception": Exception("Page not Found")}),
    path(
        "inactive/", page_not_found, kwargs={"exception": Exception("Page not Found")}
    ),
]

urlpatterns = disabled_urls + [
    # Django
    path("admin/", admin.site.urls),
    # 3rd-party
    path("", include("allauth.urls")),
    # Local
    path("", include("apps.pages.urls", namespace="pages")),
    path("", include("apps.users.urls", namespace="users")),
]

if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
