from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "get_full_name", "role", "is_department_head", "is_staff", "is_active")
    list_filter = ("role", "is_department_head", "is_staff", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("EMEC Profile", {"fields": ("role", "job_title", "phone", "avatar", "is_department_head")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("EMEC Profile", {"fields": ("role", "job_title", "phone")}),
    )

    @admin.display(description="Full name")
    def get_full_name(self, obj):
        return obj.get_full_name() or "—"
