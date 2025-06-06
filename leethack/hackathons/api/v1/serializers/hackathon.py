from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import empty

from leethack.participations.models import Participant
from leethack.core.utils import build_image_validators
from .nested import CategoryNestedSerializer
from leethack.hackathons.models import Hackathon

from leethack.users.api.v1.serializers import UserNestedSerializer


class ParticipantNestedSerializer(serializers.Serializer):
    """Nested serializer for Participant model."""

    id = serializers.UUIDField(help_text="UUID of participant.")
    user = UserNestedSerializer(help_text="Detailed representation of user.")


class BaseHackathonReadSerializer(serializers.Serializer):
    """
    Base read serializer for Hackathon model.
    Includes common fields for list and retrieve serializers.
    """

    id = serializers.UUIDField(help_text="Unique identifier of hackathon.")
    host = UserNestedSerializer(help_text="Detailed representation of host.")
    title = serializers.CharField(help_text="Name of hackathon.")
    category = CategoryNestedSerializer(
        help_text="Nested detail representation of category."
    )
    prize = serializers.IntegerField(help_text="Prize for winning hackathon.")
    start_datetime = serializers.DateTimeField(
        help_text="Timestamp when the hackathon starts."
    )
    end_datetime = serializers.DateTimeField(
        help_text="Timestamp when the hackathon ends."
    )
    winner = ParticipantNestedSerializer(
        help_text="Nested detail representation of winner."
    )
    image = serializers.ImageField(
        help_text="URL of the image stored in Cloudflare R2."
    )


class HackathonListSerializer(BaseHackathonReadSerializer):
    """Serializer for listing hackathons."""

    pass


class HackathonRetrieveSerializer(BaseHackathonReadSerializer):
    """
    Serializer for retrieving detailed hackathon info.
    Includes additional "description" field.
    """

    description = serializers.CharField(help_text="Description of hackathon.")


class HackathonCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating hackathon.
    Validates image using custom validators.
    """

    image = serializers.ImageField(
        validators=build_image_validators(settings.HACKATHON_IMAGE_CONFIG),
        help_text="Image of hackathon.",
    )

    class Meta:
        model = Hackathon
        fields = (
            "id",
            "title",
            "description",
            "category",
            "prize",
            "start_datetime",
            "end_datetime",
            "image",
        )


class HackathonUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating hackathons.
    Validates winner field against hackathon participants and image.
    """

    winner = serializers.PrimaryKeyRelatedField(
        queryset=Participant.objects.none(),
        required=False,
        help_text="UUID of Participant instance.",
    )
    image = serializers.ImageField(
        validators=build_image_validators(settings.HACKATHON_IMAGE_CONFIG),
        required=False,
        help_text="New image of hackathon.",
    )

    class Meta:
        model = Hackathon
        fields = (
            "title",
            "description",
            "category",
            "prize",
            "start_datetime",
            "end_datetime",
            "winner",
            "image",
        )
        extra_kwargs = {
            "title": {"required": False},
            "description": {"required": False},
            "category": {"required": False},
            "prize": {"required": False},
            "start_datetime": {"required": False},
            "end_datetime": {"required": False},
        }

    def __init__(self, instance=None, data=empty, **kwargs):
        # фільтрую winner учасниками поточного хакатону
        super().__init__(instance=instance, data=data, **kwargs)

        hackathon = instance

        if not hackathon:
            hackathon = self.context.get("hackathon")

        if hackathon:
            qs = Participant.objects.filter(hackathon=hackathon)
            qs = qs.select_related("user", "hackathon")
            self.fields["winner"].queryset = qs
        else:
            self.fields["winner"].queryset = Participant.objects.none()

    def validate(self, attrs):
        winner = attrs.get("winner")

        if winner and self.instance.is_active:
            raise serializers.ValidationError(
                {"winner": "Cannot set winner while hackathon is active."}
            )

        if winner:
            if not winner.hackathon == self.instance:
                raise serializers.ValidationError(
                    {
                        "winner": "Selected participant is not a participant of this hackathon."
                    }
                )

        return attrs
