from django.views.generic import TemplateView


class ComingSoonView(TemplateView):
    """Temporary placeholder until Phase 14 (Contact) implements this section."""
    template_name = "coming_soon.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["section_name"] = "Contact & Inquiries"
        return ctx
