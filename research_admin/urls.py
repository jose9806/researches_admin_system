from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.shortcuts import redirect

# Customize admin site
admin.site.site_header = getattr(settings, "ADMIN_SITE_HEADER", "Research Admin")
admin.site.site_title = getattr(
    settings, "ADMIN_SITE_TITLE", "CvLAC and GrupLAC Integration"
)
admin.site.index_title = getattr(settings, "ADMIN_INDEX_TITLE", "Research Management")

# URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    # Integration URLs under admin
    path("admin/integration/", include("integration.urls")),
]

# Debug toolbar for development
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

# Redirect root URL to admin page
urlpatterns += [
    path("", lambda request: redirect("admin:index"), name="index"),
]
