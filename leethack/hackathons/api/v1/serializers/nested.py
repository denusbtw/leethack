from rest_framework import serializers


class CategoryNestedSerializer(serializers.Serializer):
    """Nested serializer for Category model."""

    id = serializers.UUIDField(help_text="Unique identifier of category.")
    title = serializers.CharField(help_text="Name of category.")
    slug = serializers.SlugField(help_text="URL-friendly identifier.")


class HackathonNestedSerializer(serializers.Serializer):
    """Nested serializer for Hackathon model."""

    id = serializers.UUIDField(help_text="Unique identifier of hackathon.")
    title = serializers.CharField(help_text="Name of hackathon.")
    category = CategoryNestedSerializer(
        help_text="Nested detail representation of category."
    )
    image = serializers.ImageField(help_text="URL of image stored in Cloudflare R2.")
