"""
Projects -- Phase 3 minimal schema for the homepage Featured Work section.
Full case-study build (problem statement, objectives, challenges, gallery,
downloads, related projects, real Client FK) lands in Phase 7 per
docs/DATABASE_DESIGN.md.
"""
from django.db import models

from apps.core.models_base import OrderableModel, PublishableModel, SEOModel, SlugModel, TimeStampedModel
from apps.industries.models import Industry


class Project(SlugModel, SEOModel, PublishableModel, OrderableModel, TimeStampedModel):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=280)
    industry = models.ForeignKey(Industry, related_name="projects", null=True, blank=True, on_delete=models.SET_NULL)
    client_name = models.CharField(
        max_length=150, blank=True,
        help_text="Free-text for now -- becomes a FK to testimonials.Client in Phase 11.",
    )
    cover_image = models.ImageField(upload_to="projects/covers/", blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Show on the homepage featured-work section.")
    is_confidential = models.BooleanField(default=False, help_text="Hide client name on the public page.")

    slug_source_field = "title"

    class Meta(OrderableModel.Meta):
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    @property
    def display_client_name(self):
        return "" if self.is_confidential else self.client_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("projects:detail", kwargs={"slug": self.slug})
