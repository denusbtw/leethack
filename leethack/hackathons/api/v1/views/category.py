from rest_framework import generics, permissions

from ..serializers import CategoryListSerializer
from leethack.hackathons.models import Category


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
