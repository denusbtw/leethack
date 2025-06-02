from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from leethack.hackathons.models import Hackathon
from leethack.participations.models import Participant, ParticipationRequest


def resolve_hackathon_id_from_view(view):
    if hasattr(view, "get_hackathon_id"):
        return view.get_hackathon_id()
    return view.kwargs.get("hackathon_id")


def resolve_hackathon_from_obj(obj):
    match obj:
        case Hackathon():
            return obj.pk
        case Participant():
            return obj.hackathon_id
        case ParticipationRequest():
            return obj.hackathon_id
        case _:
            return None


class IsHackathonHost(BasePermission):

    def get_hackathon(self, view):
        # кешую хакатон у view, щоб зменшити кількість запитів
        # це працює тому що між запитами кеш не зберігається

        if hasattr(view, "_cached_hackathon"):
            return view._cached_hackathon

        hackathon_id = resolve_hackathon_id_from_view(view)
        hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
        view._cached_hackathon = hackathon
        return hackathon

    def has_permission(self, request, view):
        hackathon = self.get_hackathon(view)
        return request.user == hackathon.host

    def has_object_permission(self, request, view, obj):
        hackathon_id = resolve_hackathon_from_obj(obj)

        if hackathon_id:
            if (
                hasattr(view, "_cached_hackathon")
                and view._cached_hackathon.pk == hackathon_id
            ):
                hackathon = view._cached_hackathon
            else:
                hackathon = get_object_or_404(Hackathon, pk=hackathon_id)
        else:
            hackathon = self.get_hackathon(view)

        return request.user == hackathon.host if hackathon else False
