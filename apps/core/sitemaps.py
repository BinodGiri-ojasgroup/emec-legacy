"""
Central sitemap registry.

Each app that introduces URL-addressable content defines its own
`django.contrib.sitemaps.Sitemap` subclass in `apps/<app>/sitemaps.py` and
registers it here under a short key. `config/urls.py` imports only this
dict, so adding a new sitemap never touches the URLconf.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Post
from apps.industries.models import Industry
from apps.projects.models import Project
from apps.research.models import ResearchItem
from apps.services.models import Service
from apps.team.models import TeamMember


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    static_names = [
        "pages:home",
        "pages:about",
    ]

    def items(self):
        return self.static_names

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Service.objects.filter(is_active=True)


class IndustrySitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return Industry.objects.filter(is_active=True)


class ProjectSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Project.objects.filter(status=Project.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class ResearchSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return ResearchItem.objects.filter(status=ResearchItem.Status.PUBLISHED)


class BlogPostSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at


class TeamMemberSitemap(Sitemap):
    priority = 0.4
    changefreq = "yearly"

    def items(self):
        return TeamMember.objects.filter(is_active=True)


SITEMAPS = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
    "industries": IndustrySitemap,
    "projects": ProjectSitemap,
    "research": ResearchSitemap,
    "blog": BlogPostSitemap,
    "team": TeamMemberSitemap,
    # "training": TrainingSitemap,    # registered in the Training phase
    # "careers": JobListingSitemap,   # registered in the Careers phase
}
