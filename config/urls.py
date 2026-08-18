"""
EMEC — Root URL configuration.

Each business domain owns its own urls.py inside apps/<app>/urls.py and is
included here under a readable, SEO-friendly path. Namespacing every include
keeps {% url %} lookups collision-free as the site grows across phases.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from apps.core.sitemaps import SITEMAPS

admin.site.site_header = "EMEC Control Center"
admin.site.site_title = "EMEC Admin"
admin.site.index_title = "Content & Operations"

urlpatterns = [
    # Admin is mounted at a non-default path — trivial but standard hardening
    # against automated /admin/ scanning bots (see docs/SECURITY.md).
    path("control/", admin.site.urls),

    # SEO infrastructure
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # CKEditor 5 image upload endpoint — required once any model field
    # switches from plain TextField to CKEditor5Field (see settings/base.py).
    path("ckeditor5/", include("django_ckeditor_5.urls")),

    # Business-domain apps, each namespaced and independently owned.
    path("", include("apps.pages.urls", namespace="pages")),        # "", "about/"
    path("about/leadership/", include("apps.team.urls", namespace="team")),
    path("services/", include("apps.services.urls", namespace="services")),
    path("industries/", include("apps.industries.urls", namespace="industries")),
    path("projects/", include("apps.projects.urls", namespace="projects")),
    path("research/", include("apps.research.urls", namespace="research")),
    path("training/", include("apps.training.urls", namespace="training")),
    path("careers/", include("apps.careers.urls", namespace="careers")),
    path("blog/", include("apps.blog.urls", namespace="blog")),
    path("clients/", include("apps.testimonials.urls", namespace="testimonials")),
    path("resources/", include("apps.media_library.urls", namespace="media_library")),
    path("contact/", include("apps.contact.urls", namespace="contact")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("__reload__/", include("django_browser_reload.urls")),
    ]
