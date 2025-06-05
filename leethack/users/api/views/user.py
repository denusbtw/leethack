from rest_framework import generics, permissions

from django.contrib.auth import get_user_model

from leethack.users.api.serializers import MeRetrieveSerializer
from leethack.users.api.serializers.user import MeUpdateSerializer

User = get_user_model()


class MeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve the authenticated user's profile.
    PATCH: Update the authenticated user's profile.
    DELETE: Delete the authenticated user.
    Only authenticated user can perform these actions.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MeRetrieveSerializer
        return MeUpdateSerializer
