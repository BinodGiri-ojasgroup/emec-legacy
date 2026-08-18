from django.contrib import admin

from apps.services.models import Service, ServiceCategory, ServiceProcessStep


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order")
    list_editable = ("display_order",)
    prepopulated_fields = {"slug": ("name",)}


class ServiceProcessStepInline(admin.TabularInline):
    model = ServiceProcessStep
    extra = 1
    fields = ("step_number", "title", "description", "display_order")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "is_active", "display_order")
    list_editable = ("is_featured", "is_active", "display_order")
    list_filter = ("category", "is_featured", "is_active", "related_industries")
    search_fields = ("title", "summary", "description")
    filter_horizontal = ("related_industries",)
    inlines = [ServiceProcessStepInline]

    fieldsets = (
        (None, {"fields": ("category", "title", "summary", "description", "icon", "hero_image")}),
        ("Related Industries", {"fields": ("related_industries",)}),
        ("Visibility", {"fields": ("is_featured", "is_active", "display_order")}),
        ("SEO", {"fields": ("seo_title", "seo_description", "og_image", "canonical_url", "noindex"), "classes": ("collapse",)}),
    )
