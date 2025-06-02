from django.contrib import admin

from .models import Hackathon, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    ordering = ("-title",)
    readonly_fields = ("created_at", "updated_at", "slug")

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "slug"),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )


@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "prize",
        "start_datetime",
        "end_datetime",
        "host",
    )
    list_filter = ("start_datetime", "end_datetime")
    search_fields = ("title", "description")
    ordering = ("-start_datetime",)
    list_select_related = ("category", "host")
    autocomplete_fields = ("category", "host")
    date_hierarchy = "start_datetime"

    # використовую raw_id_fields замість autocomplete_fields щоб уникнути
    # довгого завантаження при великій кількості учасників
    raw_id_fields = ("winner",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "host",
                    "title",
                    "description",
                    "category",
                    "image",
                    "is_active",
                ),
            },
        ),
        (
            "Event Detail",
            {
                "fields": ("start_datetime", "end_datetime", "prize"),
            },
        ),
        (
            "Results",
            {"fields": ("winner",)},
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=...):
        readonly_fields = ["created_at", "updated_at", "is_active"]
        if obj and obj.is_active:
            return readonly_fields + ["winner"]
        return readonly_fields
