from django.conf import settings
from django.core.cache import cache

from apps.core.models import Announcement, NavigationMenu, SiteConfiguration


def site_config(request):
    """
    Global template context: site identity, navigation menus, active
    announcement banner. Navigation is cached (CACHE_TTL_LONG) since it
    changes rarely but is read on every single page render.
    """
    config = getattr(request, "site_config", None) or SiteConfiguration.load()

    nav = cache.get("nav_menus")
    if nav is None:
        nav = {
            menu.slot: menu.items.filter(parent=None, is_active=True).select_related(None).prefetch_related("children")
            for menu in NavigationMenu.objects.prefetch_related("items")
        }
        cache.set("nav_menus", nav, settings.CACHE_TTL_LONG)

    announcement = (
        Announcement.objects.filter(is_active=True).order_by("-created_at").first()
    )

    return {
        "site_config": config,
        "nav_header_primary": nav.get("header_primary"),
        "nav_header_utility": nav.get("header_utility"),
        "nav_footer_col_1": nav.get("footer_col_1"),
        "nav_footer_col_2": nav.get("footer_col_2"),
        "nav_footer_col_3": nav.get("footer_col_3"),
        "nav_footer_legal": nav.get("footer_legal"),
        "active_announcement": announcement,
    }


def seo_defaults(request):
    """
    Fallback SEO/meta values every template can rely on existing, even
    before a page-specific view overrides them via context.
    """
    return {
        "default_seo_title": settings.DEFAULT_SEO_TITLE,
        "default_seo_description": settings.DEFAULT_SEO_DESCRIPTION,
        "site_domain": settings.SITE_DOMAIN,
    }
