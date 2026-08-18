from django.urls import path

from apps.training.views import ComingSoonView

app_name = "training"

urlpatterns = [
    path("", ComingSoonView.as_view(), name="index"),
]
