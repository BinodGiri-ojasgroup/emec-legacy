from django.shortcuts import render

from apps.core.models import SiteConfiguration


class SiteConfigMiddleware:
    """
    Loads the SiteConfiguration singleton once per request and attaches it
    to `request.site_config`, so views and templates never issue their own
    query for it. Also enforces `maintenance_mode` for non-staff visitors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        config = SiteConfiguration.load()
        request.site_config = config

        if config.maintenance_mode and not (
            request.user.is_authenticated and request.user.is_staff
        ) and not request.path.startswith("/control/"):
            return render(request, "maintenance.html", status=503)

        return self.get_response(request)
