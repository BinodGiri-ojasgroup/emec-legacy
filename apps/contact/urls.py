from django.urls import path

from apps.contact.views import ComingSoonView

app_name = "contact"

urlpatterns = [
    path("", ComingSoonView.as_view(), name="index"),
]
