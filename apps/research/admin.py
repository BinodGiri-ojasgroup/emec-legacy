from django.contrib import admin

from apps.research.models import ResearchCategory, ResearchItem


@admin.register(ResearchCategory)
class ResearchCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ResearchItem)
class ResearchItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "is_featured", "publication_date")
    list_editable = ("is_featured",)
    list_filter = ("status", "category", "is_featured")
    search_fields = ("title", "abstract")
