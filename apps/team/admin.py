from django.contrib import admin

from apps.team.models import Department, TeamMember


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role_title", "department", "is_leadership", "is_active", "display_order")
    list_editable = ("is_leadership", "is_active", "display_order")
    list_filter = ("department", "is_leadership", "is_active")
    search_fields = ("name", "role_title", "bio")
