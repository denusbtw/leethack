from rest_framework import generics, permissions, filters

from leethack.hackathons.api.v1.serializers import HackathonListSerializer
from leethack.hackathons.models import Hackathon


class MyParticipatedHackathonListAPIView(generics.ListAPIView):
    """
    Returns list of hackathons where current user is participant
    """

    serializer_class = HackathonListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    # TODO: move search by description to SearchVector
    search_fields = ("title", "description")
    ordering_fields = ("start_datetime", "end_datetime", "prize")
    ordering = ("-end_datetime",)

    def get_queryset(self):
        return Hackathon.objects.filter(participants__user=self.request.user)


class MyHostedHackathonListAPIView(generics.ListAPIView):
    """
    Returns list of hackathons hosted by request.user
    """

    serializer_class = HackathonListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    # TODO: move search by description to SearchVector
    search_fields = ("title", "description")
    ordering_fields = ("start_datetime", "end_datetime", "prize")
    ordering = ("-end_datetime",)

    def get_queryset(self):
        return Hackathon.objects.filter(host=self.request.user)


class UserHostedHackathonListAPIView(generics.ListAPIView):
    """
    Returns list of hackathons hosted by user with id=`user_id`
    """

    serializer_class = HackathonListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    # TODO: move search by description to SearchVector
    search_fields = ("title", "description")
    ordering_fields = ("start_datetime", "end_datetime", "prize")
    ordering = ("-end_datetime",)

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Hackathon.objects.filter(host_id=user_id)
