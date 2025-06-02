from django.contrib import admin

from leethack.participations.models import Participant, ParticipationRequest


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "hackathon", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "hackathon__title",
    )
    ordering = ("-created_at",)
    autocomplete_fields = ("user", "hackathon")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "hackathon"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


@admin.action(description="Approve selected requests")
def approve_requests(request, queryset):
    queryset.update(status=ParticipationRequest.Status.APPROVED)


@admin.action(description="Reject selected requests")
def reject_requests(request, queryset):
    queryset.update(status=ParticipationRequest.Status.REJECTED)


@admin.register(ParticipationRequest)
class ParticipationRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "hackathon", "status", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "hackathon__title",
    )
    list_filter = ("status",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user", "hackathon")
    date_hierarchy = "created_at"

    fieldsets = (
        (
            None,
            {
                "fields": ("user", "hackathon", "status"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    actions = [approve_requests, reject_requests]
