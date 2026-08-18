from django.views.generic import TemplateView

from apps.blog.models import Post
from apps.industries.models import Industry
from apps.pages.models import (
    AboutPage,
    CoreValue,
    GroupCompany,
    HomePage,
    HomepageStatistic,
    ProcessStep,
    TimelineEvent,
)
from apps.projects.models import Project
from apps.research.models import ResearchItem
from apps.services.models import Service
from apps.team.models import TeamMember
from apps.testimonials.models import Testimonial


class HomeView(TemplateView):
    """
    Phase 3 -- full section build. Each section queries its own app's
    models directly; the HomePage singleton only supplies framing copy
    and the show_* visibility flags, so an editor can hide a section from
    Django Admin without a code change even after this is live.
    """
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        home = HomePage.load()
        ctx["home"] = home

        if home.show_statistics:
            ctx["statistics"] = HomepageStatistic.objects.filter(is_active=True)

        if home.show_capabilities:
            ctx["services"] = Service.objects.filter(is_active=True, is_featured=True).select_related("category")[:6]

        if home.show_industries:
            ctx["industries"] = Industry.objects.filter(is_active=True)[:8]

        if home.show_projects:
            ctx["projects"] = (
                Project.objects.filter(status=Project.Status.PUBLISHED, is_featured=True)
                .select_related("industry")[:3]
            )

        if home.show_research:
            ctx["research_items"] = (
                ResearchItem.objects.filter(status=ResearchItem.Status.PUBLISHED, is_featured=True)
                .select_related("category")[:2]
            )

        if home.show_process:
            ctx["process_steps"] = ProcessStep.objects.all()

        if home.show_testimonials:
            ctx["clients"] = Testimonial.objects.filter(is_featured=True).select_related("client")
            ctx["featured_testimonial"] = ctx["clients"].first()

        if home.show_news:
            ctx["news_posts"] = Post.objects.filter(status=Post.Status.PUBLISHED)[:3]

        return ctx


class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["about"] = AboutPage.load()
        ctx["values"] = CoreValue.objects.all()
        ctx["timeline"] = TimelineEvent.objects.all()
        ctx["group_companies"] = GroupCompany.objects.filter(is_active=True)
        ctx["leadership"] = TeamMember.objects.filter(is_active=True, is_leadership=True).select_related("department")
        return ctx
