from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls")),
    path("api/", include("config.api_router")),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
