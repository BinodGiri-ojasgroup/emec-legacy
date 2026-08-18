from django.views.generic import DetailView, ListView

from apps.team.models import TeamMember


class LeadershipListView(ListView):
    """Also used to hydrate the About page's leadership section directly."""
    model = TeamMember
    template_name = "team/list.html"
    context_object_name = "team_members"
    queryset = TeamMember.objects.filter(is_active=True, is_leadership=True).select_related("department")


class TeamMemberDetailView(DetailView):
    model = TeamMember
    template_name = "team/detail.html"
    context_object_name = "member"
    queryset = TeamMember.objects.filter(is_active=True)
