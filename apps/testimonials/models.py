"""
Testimonials/Clients -- Phase 3 minimal schema so the homepage "Trusted By"
section has real client logos and one featured testimonial. Full build
(Partner, Award, project linkage) lands in Phase 11.
"""
from django.db import models

from apps.core.models_base import OrderableModel, TimeStampedModel


class Client(OrderableModel, TimeStampedModel):
    name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to="clients/logos/", blank=True, null=True)
    website_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta(OrderableModel.Meta):
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name


class Testimonial(OrderableModel, TimeStampedModel):
    client = models.ForeignKey(Client, related_name="testimonials", null=True, blank=True, on_delete=models.SET_NULL)
    author_name = models.CharField(max_length=150)
    author_role = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta(OrderableModel.Meta):
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.author_name} — {self.client}"
