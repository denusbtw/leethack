from rest_framework import generics, permissions

from django.contrib.auth import get_user_model

from leethack.users.api.serializers import MeRetrieveSerializer
from leethack.users.api.serializers.user import MeUpdateSerializer

User = get_user_model()


class MeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "GET":
            return MeRetrieveSerializer
        return MeUpdateSerializer
