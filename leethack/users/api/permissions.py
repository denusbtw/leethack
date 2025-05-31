from rest_framework.permissions import BasePermission


class IsHost(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_host


class CanDeleteOwnParticipationRequest(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method == "DELETE" and obj.is_pending
