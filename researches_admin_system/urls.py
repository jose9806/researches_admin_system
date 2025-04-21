from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Keep this for any standalone integration URLs
    path("admin/integration/", include("integration.urls")),
]
