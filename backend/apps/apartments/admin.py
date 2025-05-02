from django.contrib import admin
from .models import Apartment


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "number_of_rooms",
        "square",
        "availability",
        "owner",
        "created_at",
    )
    list_filter = ("availability", "number_of_rooms", "price")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
