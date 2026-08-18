"""
EMEC Control Center — admin dashboard.

Rather than replacing Django's AdminSite wholesale (which would require
every app's admin.py to register against a custom site instance), we wrap
the default admin index view to inject a small "at a glance" stats panel.
This keeps every existing `@admin.register(...)` call working unchanged and
means new apps get dashboard cards just by adding an entry to
`DASHBOARD_SECTIONS` below — no admin.py changes required elsewhere.
"""
from django.apps import apps as django_apps


# (section label, app_label, model_name, url name for the changelist)
DASHBOARD_SECTIONS = [
    ("Navigation Items", "core", "navigationitem"),
    ("Announcements (active)", "core", "announcement"),
    ("Homepage Statistics", "pages", "homepagestatistic"),
    ("Timeline Events", "pages", "timelineevent"),
    ("Core Values", "pages", "corevalue"),
    ("Group Companies", "pages", "groupcompany"),
    ("Team Members", "team", "teammember"),
    ("Services", "services", "service"),
    ("Industries", "industries", "industry"),
    ("Projects", "projects", "project"),
    ("Research Items", "research", "researchitem"),
    ("Blog Posts", "blog", "post"),
    ("Testimonials", "testimonials", "testimonial"),
    ("Staff Accounts", "accounts", "user"),
]


def get_dashboard_stats():
    """
    Returns a list of dicts: label, count, admin changelist URL. Silently
    skips any model that isn't installed yet (later-phase apps) so this
    never breaks as apps are added incrementally.
    """
    stats = []
    for label, app_label, model_name in DASHBOARD_SECTIONS:
        try:
            model = django_apps.get_model(app_label, model_name)
        except LookupError:
            continue
        try:
            count = model.objects.count()
        except Exception:
            count = None
        stats.append({
            "label": label,
            "count": count,
            "url": f"/control/{app_label}/{model_name}/",
        })
    return stats


def patch_admin_index():
    """Wrap admin.site.index() so it always carries `dashboard_stats` in context."""
    from django.contrib import admin

    original_index = admin.site.index

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["dashboard_stats"] = get_dashboard_stats()
        return original_index(request, extra_context)

    admin.site.index = index.__get__(admin.site, admin.AdminSite)
