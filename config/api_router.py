from django.urls import path, include

app_name = "api"
urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("v1/", include("leethack.api.urls.v1")),
]