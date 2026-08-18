from django.views.generic import TemplateView


class ComingSoonView(TemplateView):
    """Full clients/partners/awards directory lands in Phase 11."""
    template_name = "coming_soon.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section_name"] = "Testimonials, Clients & Partners"
        return ctx
