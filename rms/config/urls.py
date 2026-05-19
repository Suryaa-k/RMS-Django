from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Mount the core app at the site root.
    # All restaurant URLs live under /
    path("", include("core.urls", namespace="core")),
]
