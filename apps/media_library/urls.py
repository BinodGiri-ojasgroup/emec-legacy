from django.urls import path

from apps.media_library.views import ComingSoonView

app_name = "media_library"

urlpatterns = [
    path("", ComingSoonView.as_view(), name="index"),
]
