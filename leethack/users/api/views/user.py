from rest_framework import generics, permissions

from django.contrib.auth import get_user_model

from leethack.users.api.serializers import MeRetrieveSerializer
from leethack.users.api.serializers.user import MeUpdateSerializer

User = get_user_model()


class MeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return MeRetrieveSerializer
        return MeUpdateSerializer
