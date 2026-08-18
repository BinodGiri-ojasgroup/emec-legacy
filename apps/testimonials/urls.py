from django.urls import path

from apps.testimonials.views import ComingSoonView

app_name = "testimonials"

urlpatterns = [
    path("", ComingSoonView.as_view(), name="index"),
]
