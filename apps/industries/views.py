from django.views.generic import DetailView, ListView

from apps.industries.models import Industry


class IndustryListView(ListView):
    model = Industry
    template_name = "industries/list.html"
    context_object_name = "industries"
    queryset = Industry.objects.filter(is_active=True)


class IndustryDetailView(DetailView):
    model = Industry
    template_name = "industries/detail.html"
    context_object_name = "industry"
    queryset = Industry.objects.filter(is_active=True)
