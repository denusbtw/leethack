from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "leethack"

env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))


DEBUG = env.bool("DJANGO_DEBUG", False)

TIME_ZONE = "Europe/Kyiv"

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_TZ = True


ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": env.db(
        "DATABASE_URL", default="postgres://postgres:password@localhost:5432/dev_db"
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "storages",
    "debug_toolbar",
]

LOCAL_APPS = [
    "leethack.core",
    "leethack.users",
    "leethack.hackathons",
    "leethack.participations",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


STATIC_URL = "static/"


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "leethack.api.exceptions.custom_exception_handler"
}


DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"
DEFAULT_PROFILE_BACKGROUND = "profile_backgrounds/default.jpg"

PROFILE_PICTURE_CONFIG = {
    "allowed_formats": {"jpeg", "png", "webp", "bmp"},
    "ratio": (1 / 1, "1:1"),
    "min_width": 192,
    "min_height": 192,
    "max_size_mb": 2,
}

PROFILE_BACKGROUND_CONFIG = {
    "allowed_formats": {"jpeg", "png", "webp", "bmp"},
    "ratio": (16 / 9, "16:9"),
    "min_width": 1920,
    "min_height": 1080,
    "max_size_mb": 7,
}

AWS_ACCOUNT_ID = env("AWS_ACCOUNT_ID")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = f"https://{AWS_ACCOUNT_ID}.r2.cloudflarestorage.com"


# TODO: чомусь не можна подивитись картинку, помилка
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


INTERNAL_IPS = [
    "127.0.0.1",
]
