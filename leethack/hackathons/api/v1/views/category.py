from rest_framework import generics, filters

from .pagination import CategoryPagination
from ..serializers import CategoryListSerializer
from leethack.hackathons.models import Category


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = CategoryPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ("title",)
    ordering_fields = ("title",)
    ordering = ("title",)
