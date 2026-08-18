from django.views.generic import DetailView, ListView

from apps.research.models import ResearchItem


class ResearchListView(ListView):
    model = ResearchItem
    template_name = "research/list.html"
    context_object_name = "items"
    queryset = ResearchItem.objects.filter(status=ResearchItem.Status.PUBLISHED).select_related("category")


class ResearchDetailView(DetailView):
    model = ResearchItem
    template_name = "research/detail.html"
    context_object_name = "item"
    queryset = ResearchItem.objects.filter(status=ResearchItem.Status.PUBLISHED)
