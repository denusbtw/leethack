import os

import dj_database_url

from .base import *


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = [".onrender.com", "localhost", "127.0.0.1"]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + [
    m for m in MIDDLEWARE if m not in ["django.middleware.security.SecurityMiddleware"]
]


if "PROD_DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.parse(
            os.environ.get("PROD_DATABASE_URL"),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
