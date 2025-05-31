from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from leethack.core.models import UUIDModel, TimestampedModel


class Participant(UUIDModel, TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participants",
        help_text=_("User who is participant"),
    )
    hackathon = models.ForeignKey(
        "hackathons.Hackathon",
        on_delete=models.CASCADE,
        related_name="participants",
        help_text=_("Hackathon this user is participant of."),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "hackathon"), name="unique_participant_user_hackathon"
            )
        ]

    def __str__(self):
        return f"{self.user.username} in {self.hackathon.title}"


class ParticipationRequest(UUIDModel, TimestampedModel):
    class Status(models.TextChoices):
        APPROVED = ("approved", "Approved")
        PENDING = ("pending", "Pending")
        REJECTED = ("rejected", "Rejected")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="participation_requests",
        help_text=_("User who sent request"),
    )
    hackathon = models.ForeignKey(
        "hackathons.Hackathon",
        on_delete=models.CASCADE,
        related_name="participation_requests",
        help_text=_("Hackathon this user is participant of."),
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        help_text=_("Status of request."),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "hackathon"),
                name="unique_participation_request_user_hackathon",
            )
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.hackathon.title} [{self.status}]"

    @property
    def is_approved(self):
        return self.status == self.Status.APPROVED

    @property
    def is_pending(self):
        return self.status == self.Status.PENDING

    @property
    def is_rejected(self):
        return self.status == self.Status.REJECTED
