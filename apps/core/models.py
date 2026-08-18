from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from apps.core.models_base import OrderableModel, TimeStampedModel


class SingletonModel(models.Model):
    """
    Base for "there can only be one" content, e.g. SiteConfiguration or the
    Homepage. Enforces a single row at the DB/application level and exposes
    `.load()` so templates/views never have to think about primary keys.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singletons are never deleted, only edited

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteConfiguration(SingletonModel, TimeStampedModel):
    """
    Global, site-wide settings editable from a single Django Admin screen:
    identity, contact defaults, footer copy, tracking codes, feature flags.
    This is what `apps.core.context_processors.site_config` injects into
    every template context.
    """

    # Identity
    site_name = models.CharField(max_length=150, default="Electro Mnemonic Engineering Consultancy")
    short_name = models.CharField(max_length=50, default="EMEC")
    tagline = models.CharField(max_length=200, blank=True, help_text="Short brand line used near the logo/footer.")
    founding_year_bs = models.CharField(max_length=10, default="2070")
    founding_year_ad = models.PositiveIntegerField(default=2013)
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    logo_dark = models.ImageField(
        upload_to="branding/", blank=True, null=True,
        help_text="Optional alternate logo for dark backgrounds/dark mode.",
    )
    favicon = models.ImageField(upload_to="branding/", blank=True, null=True)

    # Default contact info (individual offices are managed in apps.contact)
    primary_email = models.EmailField(default="info@emec.com.np")
    primary_phone = models.CharField(max_length=30, default="+977-1-0000000")
    whatsapp_number = models.CharField(max_length=30, blank=True)

    # Footer
    footer_about_text = models.TextField(blank=True)
    footer_copyright_text = models.CharField(
        max_length=255, blank=True,
        help_text="e.g. '© {year} EMEC — Electro Mnemonic Engineering Consultancy'",
    )

    # Group / sister companies (for the 'Our Group' footer/about block)
    group_intro_text = models.TextField(
        blank=True,
        help_text="Short intro explaining EMEC as the parent of the group (Nepal Agro Yantra, Ojas Solutions, RC Interior…).",
    )

    # Analytics / tracking
    google_analytics_id = models.CharField(max_length=30, blank=True)
    google_tag_manager_id = models.CharField(max_length=30, blank=True)
    meta_pixel_id = models.CharField(max_length=30, blank=True)

    # Default SEO / social
    default_og_image = models.ImageField(upload_to="seo/", blank=True, null=True)
    default_meta_description = models.CharField(max_length=160, blank=True)

    # Feature flags — lets non-technical staff toggle major sections without
    # a deploy while a section is still being populated with content.
    show_careers = models.BooleanField(default=True)
    show_blog = models.BooleanField(default=True)
    show_research = models.BooleanField(default=True)
    show_training = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return "Site Configuration"


class SocialLink(OrderableModel, TimeStampedModel):
    class Platform(models.TextChoices):
        FACEBOOK = "facebook", "Facebook"
        LINKEDIN = "linkedin", "LinkedIn"
        INSTAGRAM = "instagram", "Instagram"
        YOUTUBE = "youtube", "YouTube"
        TWITTER_X = "twitter_x", "X (Twitter)"
        GITHUB = "github", "GitHub"
        TIKTOK = "tiktok", "TikTok"

    platform = models.CharField(max_length=20, choices=Platform.choices, unique=True)
    url = models.URLField()
    is_active = models.BooleanField(default=True)

    class Meta(OrderableModel.Meta):
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"

    def __str__(self):
        return self.get_platform_display()


class NavigationMenu(TimeStampedModel):
    """
    A named menu (Primary Header, Footer Column 1, Footer Column 2, Mobile…)
    so marketing can restructure navigation entirely from Django Admin.
    """

    SLOT_CHOICES = [
        ("header_primary", "Header — Primary"),
        ("header_utility", "Header — Utility (top bar)"),
        ("footer_col_1", "Footer — Column 1"),
        ("footer_col_2", "Footer — Column 2"),
        ("footer_col_3", "Footer — Column 3"),
        ("footer_legal", "Footer — Legal row"),
    ]
    slot = models.CharField(max_length=30, choices=SLOT_CHOICES, unique=True)
    label = models.CharField(max_length=100, help_text="Internal label, not shown on site.")

    class Meta:
        verbose_name = "Navigation Menu"
        verbose_name_plural = "Navigation Menus"

    def __str__(self):
        return self.get_slot_display()


class NavigationItem(MPTTModel, TimeStampedModel):
    """
    Tree-structured menu items (supports one level of dropdown, e.g.
    Services -> Engineering Consulting / R&D / Automation…). Can point to a
    manual URL, or resolve dynamically to any object exposing get_absolute_url
    via the generic `linked_object` fields — kept simple in Phase 1 with a
    manual URL/named-route pair, extended in later phases as needed.
    """

    menu = models.ForeignKey(NavigationMenu, related_name="items", on_delete=models.CASCADE)
    parent = TreeForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    url = models.CharField(
        max_length=255, blank=True,
        help_text="Absolute path (/services/) or full URL. Leave blank if this is a dropdown-only parent.",
    )
    open_in_new_tab = models.BooleanField(default=False)
    icon = models.CharField(max_length=50, blank=True, help_text="Optional icon identifier from the UI kit.")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["display_order"]

    class Meta:
        verbose_name = "Navigation Item"
        verbose_name_plural = "Navigation Items"

    def __str__(self):
        return f"{self.menu.get_slot_display()} → {self.label}"

    def clean(self):
        if self.parent and self.parent.menu_id != self.menu_id:
            raise ValidationError("A navigation item's parent must belong to the same menu.")


class Announcement(TimeStampedModel):
    """
    Optional slim banner at the very top of the site — e.g. 'Applications
    open for the Q3 Embedded Systems Workshop'. Editors turn it on/off
    without needing a deploy.
    """

    message = models.CharField(max_length=200)
    link_label = models.CharField(max_length=50, blank=True)
    link_url = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=False)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Announcement Banner"
        verbose_name_plural = "Announcement Banner"

    def __str__(self):
        return self.message
