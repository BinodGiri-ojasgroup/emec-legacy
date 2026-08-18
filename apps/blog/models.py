"""
Blog/News -- Phase 3 minimal schema for the homepage "Latest News" section.
Full build (authors, tags, comments, related posts) lands in Phase 12.
"""
from django.db import models

from apps.core.models_base import PublishableModel, SEOModel, SlugModel, TimeStampedModel


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class Post(SlugModel, SEOModel, PublishableModel, TimeStampedModel):
    category = models.ForeignKey(BlogCategory, related_name="posts", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=280)
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    slug_source_field = "title"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog:detail", kwargs={"slug": self.slug})
