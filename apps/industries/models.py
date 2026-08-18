"""
Industries -- Phase 3 minimal schema for the homepage Industries grid.
Full build (related services M2M, related projects reverse relation, hero
imagery) lands in Phase 6.
"""
from django.db import models

from apps.core.models_base import OrderableModel, SlugModel, TimeStampedModel


class Industry(SlugModel, OrderableModel, TimeStampedModel):
    name = models.CharField(max_length=120)
    summary = models.CharField(max_length=280, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to="industries/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    slug_source_field = "name"

    class Meta(OrderableModel.Meta):
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("industries:detail", kwargs={"slug": self.slug})
