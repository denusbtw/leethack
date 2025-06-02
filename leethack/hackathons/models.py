from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

from leethack.core.models import UUIDModel, TimestampedModel

User = get_user_model()


class Category(UUIDModel, TimestampedModel):
    title = models.CharField(
        max_length=255, unique=True, help_text=_("Title of category.")
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Hackathon(UUIDModel, TimestampedModel):
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="hosted_hackathons",
        help_text=_("Organizer of hackathon."),
    )
    title = models.CharField(max_length=255, help_text=_("Title of hackathon."))
    description = models.TextField(help_text=_("Description of hackathon."))
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        help_text=_("Category of hackathon."),
    )
    prize = models.PositiveIntegerField(help_text=_("Prize for winning hackathon."))
    start_datetime = models.DateTimeField(
        help_text=_("Start date and time of hackathon.")
    )
    end_datetime = models.DateTimeField(help_text=_("End date and time of hackathon."))
    winner = models.ForeignKey(
        "participations.Participant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="won_hackathons",
    )
    # TODO: генерувати унікальні імена для файлів
    image = models.ImageField(upload_to="hackathons/")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(start_datetime__lt=models.F("end_datetime")),
                name="end_datetime_after_start_datetime",
            )
        ]

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        from django.utils import timezone

        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime
