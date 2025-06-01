from rest_framework import serializers


class CategoryNestedSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    slug = serializers.SlugField()


class HackathonNestedSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    category = CategoryNestedSerializer()
    image = serializers.ImageField()
