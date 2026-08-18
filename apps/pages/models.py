from django.db import models

from apps.core.models import SingletonModel
from apps.core.models_base import OrderableModel, SEOModel, TimeStampedModel


class HomePage(SingletonModel, SEOModel, TimeStampedModel):
    """
    Every homepage block is a field or a related, orderable model — nothing
    on the homepage is hardcoded in a template. Editors control copy,
    imagery, and which sections are visible from a single Django Admin page.
    """

    # Hero
    hero_eyebrow = models.CharField(max_length=80, blank=True, help_text="Small label above the headline, e.g. 'Since 2070 B.S.'")
    hero_headline = models.CharField(max_length=200, default="Engineering the foundation of what's next.")
    hero_subheadline = models.TextField(blank=True)
    hero_video = models.FileField(upload_to="homepage/hero/", blank=True, null=True)
    hero_image = models.ImageField(upload_to="homepage/hero/", blank=True, null=True)
    hero_primary_cta_label = models.CharField(max_length=50, default="Start a Consultation")
    hero_primary_cta_url = models.CharField(max_length=255, default="/contact/")
    hero_secondary_cta_label = models.CharField(max_length=50, blank=True, default="View Our Work")
    hero_secondary_cta_url = models.CharField(max_length=255, blank=True, default="/projects/")

    # Section intros (the section *content* — projects, services, testimonials
    # — is pulled live from those apps; this is just the framing copy)
    capabilities_heading = models.CharField(max_length=150, default="Engineering Capabilities")
    capabilities_intro = models.TextField(blank=True)

    industries_heading = models.CharField(max_length=150, default="Industries We Serve")
    industries_intro = models.TextField(blank=True)

    projects_heading = models.CharField(max_length=150, default="Featured Work")
    projects_intro = models.TextField(blank=True)

    research_heading = models.CharField(max_length=150, default="Research & Innovation")
    research_intro = models.TextField(blank=True)

    process_heading = models.CharField(max_length=150, default="How We Engineer Solutions")
    process_intro = models.TextField(blank=True)

    training_heading = models.CharField(max_length=150, default="Training & Knowledge Transfer")
    training_intro = models.TextField(blank=True)

    testimonials_heading = models.CharField(max_length=150, default="Trusted By")

    cta_heading = models.CharField(max_length=150, default="Have an engineering challenge?")
    cta_body = models.TextField(blank=True)
    cta_button_label = models.CharField(max_length=50, default="Talk to Our Engineers")
    cta_button_url = models.CharField(max_length=255, default="/contact/")

    # Section visibility toggles — editors can hide a section that isn't
    # populated yet without needing a code deploy.
    show_statistics = models.BooleanField(default=True)
    show_capabilities = models.BooleanField(default=True)
    show_industries = models.BooleanField(default=True)
    show_projects = models.BooleanField(default=True)
    show_research = models.BooleanField(default=True)
    show_process = models.BooleanField(default=True)
    show_training = models.BooleanField(default=True)
    show_testimonials = models.BooleanField(default=True)
    show_news = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Homepage"
        verbose_name_plural = "Homepage"

    def __str__(self):
        return "Homepage Content"


class HomepageStatistic(OrderableModel, TimeStampedModel):
    """e.g. '12+ Years', '150+ Projects Delivered', '40 Engineers'."""

    value = models.CharField(max_length=20, help_text="e.g. '150+', '12', '98%'")
    label = models.CharField(max_length=100, help_text="e.g. 'Projects Delivered'")
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta(OrderableModel.Meta):
        verbose_name = "Homepage Statistic"
        verbose_name_plural = "Homepage Statistics"

    def __str__(self):
        return f"{self.value} {self.label}"


class AboutPage(SingletonModel, SEOModel, TimeStampedModel):
    """Singleton content for /about/ — story, vision, mission."""

    intro_heading = models.CharField(max_length=200, default="Where Our Group Began")
    story = models.TextField(
        help_text="The EMEC origin story — founded 2070 B.S. (2013), first company in the group.",
        blank=True,
    )
    vision_statement = models.TextField(blank=True)
    mission_statement = models.TextField(blank=True)
    group_story = models.TextField(
        blank=True,
        help_text="Explains how EMEC's engineering foundation gave rise to Nepal Agro Yantra, Ojas Solutions, RC Interior, and future ventures.",
    )
    hero_image = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Page"

    def __str__(self):
        return "About Page Content"


class CoreValue(OrderableModel, TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.title


class TimelineEvent(OrderableModel, TimeStampedModel):
    """
    Company history / innovation timeline — used on both the homepage
    highlight strip and the full About/History page.
    """

    year_bs = models.CharField(max_length=10, blank=True)
    year_ad = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="timeline/", blank=True, null=True)
    is_milestone = models.BooleanField(default=False, help_text="Highlight this as a major milestone on the timeline.")

    class Meta(OrderableModel.Meta):
        verbose_name = "Timeline Event"
        verbose_name_plural = "Timeline Events"

    def __str__(self):
        return f"{self.year_ad} — {self.title}"


class ProcessStep(OrderableModel, TimeStampedModel):
    """
    'How We Engineer Solutions' — the one place on the homepage where
    numbered markers are appropriate, because this content is a real,
    ordered sequence (see docs/DESIGN_SYSTEM.md).
    """

    step_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta(OrderableModel.Meta):
        verbose_name = "Process Step"
        verbose_name_plural = "Process Steps"

    def __str__(self):
        return f"{self.step_number}. {self.title}"


class GroupCompany(OrderableModel, TimeStampedModel):
    """
    The sister companies EMEC's engineering capability made possible
    (Nepal Agro Yantra, Ojas Solutions, RC Interior, future ventures) —
    shown in an 'Our Group' section to reinforce EMEC as the parent
    engineering powerhouse.
    """

    name = models.CharField(max_length=150)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="group/", blank=True, null=True)
    website_url = models.URLField(blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta(OrderableModel.Meta):
        verbose_name = "Group Company"
        verbose_name_plural = "Group Companies"

    def __str__(self):
        return self.name
