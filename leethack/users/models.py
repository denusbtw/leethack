import os

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from leethack.core.models import UUIDModel
from leethack.core.utils import generate_unique_filename


class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(
            email, username=username, password=password, **extra_fields
        )


def upload_profile_picture(instance, filename):
    unique_filename = generate_unique_filename(filename)
    return os.path.join("profile_pictures/", unique_filename)


def upload_profile_background(instance, filename):
    unique_filename = generate_unique_filename(filename)
    return os.path.join("profile_backgrounds/", unique_filename)


class User(UUIDModel, AbstractUser):
    class Role(models.TextChoices):
        USER = ("user", "User")
        HOST = ("host", "Host")

    email = models.EmailField(_("email_address"), unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        help_text=_("Optional username, defaults to the email before @ if not set."),
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        help_text=_("Role of the user in the system."),
    )
    profile_picture = models.ImageField(
        upload_to=upload_profile_picture,
        blank=True,
        default=settings.DEFAULT_PROFILE_PICTURE,
    )
    profile_background = models.ImageField(
        upload_to=upload_profile_background,
        blank=True,
        default=settings.DEFAULT_PROFILE_BACKGROUND,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    # TODO: add resize of profile_picture and profile_background, convert to JPEG

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    @property
    def is_host(self):
        return self.role == self.Role.HOST
