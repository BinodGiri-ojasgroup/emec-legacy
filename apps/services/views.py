from django.views.generic import DetailView, ListView

from apps.services.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/list.html"
    context_object_name = "services"
    queryset = Service.objects.filter(is_active=True).select_related("category")


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/detail.html"
    context_object_name = "service"
    queryset = Service.objects.filter(is_active=True).select_related("category").prefetch_related(
        "process_steps", "related_industries"
    )
