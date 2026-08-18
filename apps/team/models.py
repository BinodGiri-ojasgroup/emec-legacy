"""
Team -- leadership and staff profiles. Powers the About page's Leadership
section and (from Phase 8/12 onward) becomes the FK target for
ResearchItem.authors and BlogAuthor.team_member.
"""
from django.db import models

from apps.core.models_base import OrderableModel, SlugModel, TimeStampedModel


class Department(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["name"]

    def __str__(self):
        return self.name


class TeamMember(SlugModel, OrderableModel, TimeStampedModel):
    name = models.CharField(max_length=150)
    role_title = models.CharField(max_length=150)
    department = models.ForeignKey(Department, related_name="members", null=True, blank=True, on_delete=models.SET_NULL)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_leadership = models.BooleanField(default=False, help_text="Show in the About page Leadership section.")
    is_active = models.BooleanField(default=True)

    slug_source_field = "name"

    class Meta(OrderableModel.Meta):
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} — {self.role_title}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("team:detail", kwargs={"slug": self.slug})
