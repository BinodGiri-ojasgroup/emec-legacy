from django.contrib import admin

from apps.pages.models import (
    AboutPage,
    CoreValue,
    GroupCompany,
    HomePage,
    HomepageStatistic,
    ProcessStep,
    TimelineEvent,
)


class SingletonAdminMixin:
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomePage)
class HomePageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ("Hero", {"fields": (
            "hero_eyebrow", "hero_headline", "hero_subheadline", "hero_video", "hero_image",
            "hero_primary_cta_label", "hero_primary_cta_url",
            "hero_secondary_cta_label", "hero_secondary_cta_url",
        )}),
        ("Section Copy", {"fields": (
            "capabilities_heading", "capabilities_intro",
            "industries_heading", "industries_intro",
            "projects_heading", "projects_intro",
            "research_heading", "research_intro",
            "process_heading", "process_intro",
            "training_heading", "training_intro",
            "testimonials_heading",
        )}),
        ("Closing CTA", {"fields": ("cta_heading", "cta_body", "cta_button_label", "cta_button_url")}),
        ("Section Visibility", {"fields": (
            "show_statistics", "show_capabilities", "show_industries", "show_projects",
            "show_research", "show_process", "show_training", "show_testimonials", "show_news",
        )}),
        ("SEO", {"fields": ("seo_title", "seo_description", "og_image", "canonical_url", "noindex"), "classes": ("collapse",)}),
    )


@admin.register(HomepageStatistic)
class HomepageStatisticAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "is_active", "display_order")
    list_editable = ("is_active", "display_order")


@admin.register(AboutPage)
class AboutPageAdmin(SingletonAdminMixin, admin.ModelAdmin):
    fieldsets = (
        ("Story", {"fields": ("intro_heading", "story", "hero_image")}),
        ("Vision & Mission", {"fields": ("vision_statement", "mission_statement")}),
        ("Our Group", {"fields": ("group_story",)}),
        ("SEO", {"fields": ("seo_title", "seo_description", "og_image", "canonical_url", "noindex"), "classes": ("collapse",)}),
    )


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ("title", "display_order")
    list_editable = ("display_order",)


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ("year_ad", "title", "is_milestone", "display_order")
    list_editable = ("display_order",)
    list_filter = ("is_milestone",)


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("step_number", "title", "display_order")
    list_editable = ("display_order",)


@admin.register(GroupCompany)
class GroupCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "founded_year", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
