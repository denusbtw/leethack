from django.urls import path, include

from leethack.hackathons.api.v1.views import (
    HackathonListCreateAPIView,
    HackathonDetailAPIView,
    CategoryListAPIView,
)
from leethack.participations.api.v1.views import (
    HackathonParticipationRequestListCreateAPIView,
    HackathonParticipationRequestDetailAPIView,
    HackathonParticipantListAPIView,
    HackathonParticipantDetailAPIView,
)
from leethack.users.api.v1.views import (
    MyParticipationRequestListAPIView,
    MyParticipationRequestDetailAPIView,
    MyParticipationListAPIView,
    MyHostedHackathonListAPIView,
    UserHostedHackathonListAPIView,
    MyParticipatedHackathonListAPIView,
    MeDetailAPIView,
    MyParticipationDetailAPIView,
)


hackathon_urlpatterns = [
    path("", HackathonListCreateAPIView.as_view(), name="hackathon_list"),
    path(
        "<uuid:pk>/",
        HackathonDetailAPIView.as_view(),
        name="hackathon_detail",
    ),
    path(
        "<uuid:hackathon_id>/participants/",
        HackathonParticipantListAPIView.as_view(),
        name="hackathon_participant_list",
    ),
    path(
        "<uuid:hackathon_id>/participants/<uuid:pk>/",
        HackathonParticipantDetailAPIView.as_view(),
        name="hackathon_participant_detail",
    ),
    path(
        "<uuid:hackathon_id>/requests/",
        HackathonParticipationRequestListCreateAPIView.as_view(),
        name="hackathon_participation_request_list",
    ),
    path(
        "<uuid:hackathon_id>/requests/<uuid:pk>/",
        HackathonParticipationRequestDetailAPIView.as_view(),
        name="hackathon_participation_request_detail",
    ),
]

category_patterns = [
    path("", CategoryListAPIView.as_view(), name="category_list"),
]

me_urlpatterns = [
    path("", MeDetailAPIView.as_view(), name="me_detail"),
    path(
        "requests/",
        MyParticipationRequestListAPIView.as_view(),
        name="my_participation_request_list",
    ),
    path(
        "requests/<uuid:pk>/",
        MyParticipationRequestDetailAPIView.as_view(),
        name="my_participation_request_detail",
    ),
    path(
        "participations/",
        MyParticipationListAPIView.as_view(),
        name="my_participation_list",
    ),
    path(
        "participations/<uuid:pk>/",
        MyParticipationDetailAPIView.as_view(),
        name="my_participation_detail",
    ),
    path(
        "hosted-hackathons/",
        MyHostedHackathonListAPIView.as_view(),
        name="my_hosted_hackathon_list",
    ),
    path(
        "participated-hackathons/",
        MyParticipatedHackathonListAPIView.as_view(),
        name="my_participated_hackathon_list",
    ),
]

user_urlpatterns = [
    path(
        "<uuid:user_id>/hackathons/",
        UserHostedHackathonListAPIView.as_view(),
        name="user_hosted_hackathon_list",
    ),
]

app_name = "v1"
urlpatterns = [
    path("hackathons/", include(hackathon_urlpatterns)),
    path("categories/", include(category_patterns)),
    path("me/", include(me_urlpatterns)),
    path("users/", include(user_urlpatterns)),
]
