from django.contrib import admin

from apps.industries.models import Industry


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    search_fields = ("name", "summary")
