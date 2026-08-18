"""
Abstract base models shared by every app.

Keeping these in `apps.core` (rather than redefining fields per-app) is the
single most important architectural decision in this project: it guarantees
every editable model — projects, research items, jobs, blog posts, training
programs — behaves consistently in Django Admin, in querysets, and in SEO
output, from Phase 1 onward. No app should define its own `created_at`,
`slug`, or meta-title field; it should inherit one of these instead.
"""
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """created_at / updated_at on every content model, for free."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """
    Auto-slugging base. `slug_source_field` names the field to derive the
    slug from; subclasses override it (most use `title`, some use `name`).
    """

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    slug_source_field = "title"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            source = getattr(self, self.slug_source_field, "") or ""
            base_slug = slugify(source)[:240]
            slug = base_slug
            ModelClass = self.__class__
            counter = 2
            while ModelClass.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class PublishableModel(models.Model):
    """
    Draft/scheduled/published workflow. Every visitor-facing model
    (projects, research, jobs, blog posts, training programs, events) uses
    this so non-technical staff can prepare content ahead of time in Django
    Admin without it appearing on the live site.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SCHEDULED = "scheduled", "Scheduled"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True

    @property
    def is_live(self):
        from django.utils import timezone
        return self.status == self.Status.PUBLISHED and (
            self.published_at is None or self.published_at <= timezone.now()
        )


class OrderableModel(models.Model):
    """Manual drag-orderable content (services, industries, timeline items…)."""

    display_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ["display_order", "id"]


class SEOModel(models.Model):
    """
    Per-page/per-object SEO overrides. Falls back to sensible generated
    defaults (see `resolved_seo_title` etc.) so editors never *have* to fill
    these in, but can override any of them from Django Admin when they do.
    """

    seo_title = models.CharField(
        max_length=70, blank=True,
        help_text="Overrides the auto-generated <title>. Aim for ≤60 characters.",
    )
    seo_description = models.CharField(
        max_length=160, blank=True,
        help_text="Meta description shown in search results. Aim for ≤155 characters.",
    )
    og_image = models.ImageField(
        upload_to="seo/og/", blank=True, null=True,
        help_text="1200×630 recommended. Falls back to the site default OG image.",
    )
    canonical_url = models.URLField(blank=True, help_text="Leave blank unless this content is duplicated elsewhere.")
    noindex = models.BooleanField(default=False, help_text="Exclude this page from search engines.")

    class Meta:
        abstract = True

    def resolved_seo_title(self, fallback: str) -> str:
        return self.seo_title or fallback

    def resolved_seo_description(self, fallback: str) -> str:
        return self.seo_description or fallback


class AddressModel(models.Model):
    """Reused by Office, and any future model needing a physical address."""

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default="Nepal")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def full_address(self):
        parts = [self.address_line_1, self.address_line_2, self.city, self.state_province, self.postal_code, self.country]
        return ", ".join(p for p in parts if p)
