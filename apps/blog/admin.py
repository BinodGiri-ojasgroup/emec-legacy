from django.contrib import admin

from apps.blog.models import BlogCategory, Post


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "is_featured", "published_at")
    list_editable = ("is_featured",)
    list_filter = ("status", "category", "is_featured")
    search_fields = ("title", "excerpt")
