from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views import defaults


# Disable unused urls from 3rd party libraries
disabled_urls = [
    path(
        "email/",
        defaults.page_not_found,
        kwargs={"exception": Exception("Page not Found")},
    ),
    path(
        "inactive/",
        defaults.page_not_found,
        kwargs={"exception": Exception("Page not Found")},
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
    path("quizzes/", include("apps.quizzes.urls", namespace="quizzes")),
    path("", include("apps.takes.urls", namespace="takes")),
    path("review/", include("apps.reviews.urls", namespace="reviews")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            defaults.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            defaults.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            defaults.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", defaults.server_error),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
