from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.core.models import (
    Announcement,
    NavigationItem,
    NavigationMenu,
    SiteConfiguration,
    SocialLink,
)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Only one instance ever exists — admin blocks add/delete entirely."""

    fieldsets = (
        ("Identity", {"fields": ("site_name", "short_name", "tagline", "founding_year_bs", "founding_year_ad", "logo", "logo_dark", "favicon")}),
        ("Contact Defaults", {"fields": ("primary_email", "primary_phone", "whatsapp_number")}),
        ("Footer", {"fields": ("footer_about_text", "footer_copyright_text", "group_intro_text")}),
        ("Tracking", {"fields": ("google_analytics_id", "google_tag_manager_id", "meta_pixel_id")}),
        ("SEO Defaults", {"fields": ("default_og_image", "default_meta_description")}),
        ("Feature Flags", {"fields": ("show_careers", "show_blog", "show_research", "show_training", "maintenance_mode")}),
    )

    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "is_active", "display_order")
    list_editable = ("is_active", "display_order")


class NavigationItemInline(admin.TabularInline):
    model = NavigationItem
    extra = 1
    fields = ("label", "url", "parent", "display_order", "is_active", "open_in_new_tab")


@admin.register(NavigationMenu)
class NavigationMenuAdmin(admin.ModelAdmin):
    list_display = ("label", "slot")
    inlines = [NavigationItemInline]


@admin.register(NavigationItem)
class NavigationItemAdmin(DraggableMPTTAdmin):
    list_display = ("tree_actions", "indented_title", "menu", "url", "is_active")
    list_display_links = ("indented_title",)
    list_filter = ("menu", "is_active")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("message", "is_active", "starts_at", "ends_at")
    list_editable = ("is_active",)
