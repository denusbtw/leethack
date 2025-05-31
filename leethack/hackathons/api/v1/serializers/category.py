from rest_framework import serializers


class CategoryListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    slug = serializers.SlugField()
