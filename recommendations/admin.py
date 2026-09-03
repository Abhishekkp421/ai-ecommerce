from django.contrib import admin
from .models import UserInteraction


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "interaction_type",
        "created_at",
    )

    list_filter = (
        "interaction_type",
        "created_at",
    )

    search_fields = (
        "user__username",
        "product__name",
    )
