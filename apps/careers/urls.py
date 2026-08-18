from django.urls import path

from apps.careers.views import ComingSoonView

app_name = "careers"

urlpatterns = [
    path("", ComingSoonView.as_view(), name="index"),
]
