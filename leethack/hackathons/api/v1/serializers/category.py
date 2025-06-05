from rest_framework import serializers


class CategoryListSerializer(serializers.Serializer):
    """Serializer for listing categories."""

    id = serializers.UUIDField(help_text="Unique identifier of the category.")
    title = serializers.CharField(help_text="Name of the category.")
    slug = serializers.SlugField(help_text="URL-friendly identifier.")
