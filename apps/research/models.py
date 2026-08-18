"""
Research -- Phase 3 minimal schema for the homepage Research highlights.
Full build (authors M2M, PDF uploads, patents, external DOI links) lands
in Phase 8.
"""
from django.db import models

from apps.core.models_base import OrderableModel, PublishableModel, SlugModel, TimeStampedModel


class ResearchCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name = "Research Category"
        verbose_name_plural = "Research Categories"

    def __str__(self):
        return self.name


class ResearchItem(SlugModel, PublishableModel, OrderableModel, TimeStampedModel):
    category = models.ForeignKey(ResearchCategory, related_name="items", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    abstract = models.CharField(max_length=320)
    cover_image = models.ImageField(upload_to="research/covers/", blank=True, null=True)
    publication_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on the homepage research section.")

    slug_source_field = "title"

    class Meta(OrderableModel.Meta):
        verbose_name = "Research Item"
        verbose_name_plural = "Research Items"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("research:detail", kwargs={"slug": self.slug})
