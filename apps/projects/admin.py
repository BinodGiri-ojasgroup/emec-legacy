from django.contrib import admin

from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "industry", "status", "is_featured", "is_confidential", "display_order")
    list_editable = ("is_featured", "display_order")
    list_filter = ("status", "industry", "is_featured", "is_confidential")
    search_fields = ("title", "summary", "client_name")
