"""
Services -- full Phase 5 build. Extends the minimal Phase 3 schema (title,
summary, icon, category, is_featured) with SEO, rich-text description, hero
imagery, a per-service ordered process, and related industries -- the same
Service/ServiceCategory models, not a replacement.
"""
from django.db import models

from apps.core.models_base import OrderableModel, SEOModel, SlugModel, TimeStampedModel
from apps.industries.models import Industry


class ServiceCategory(OrderableModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=280, blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Service(SlugModel, SEOModel, OrderableModel, TimeStampedModel):
    category = models.ForeignKey(ServiceCategory, related_name="services", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)
    summary = models.CharField(max_length=280, help_text="One or two sentences -- shown on cards.")
    description = models.TextField(
        blank=True,
        help_text="Full service description shown on the detail page. Rich text editing lands with the CKEditor pass; plain text/paragraphs render fine today.",
    )
    icon = models.CharField(max_length=50, blank=True, help_text="Icon identifier from the UI kit.")
    hero_image = models.ImageField(upload_to="services/hero/", blank=True, null=True)
    related_industries = models.ManyToManyField(Industry, related_name="related_services", blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on the homepage capabilities grid.")
    is_active = models.BooleanField(default=True)

    slug_source_field = "title"

    class Meta(OrderableModel.Meta):
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("services:detail", kwargs={"slug": self.slug})


class ServiceProcessStep(OrderableModel, TimeStampedModel):
    """
    Per-service ordered process (e.g. how *this specific* service is
    delivered) -- distinct from pages.ProcessStep, which is the single
    global 'How We Engineer Solutions' sequence on the homepage.
    """

    service = models.ForeignKey(Service, related_name="process_steps", on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name = "Service Process Step"
        verbose_name_plural = "Service Process Steps"

    def __str__(self):
        return f"{self.service.title} — Step {self.step_number}: {self.title}"
