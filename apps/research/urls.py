from django.urls import path

from apps.research.views import ResearchDetailView, ResearchListView

app_name = "research"

urlpatterns = [
    path("", ResearchListView.as_view(), name="index"),
    path("<slug:slug>/", ResearchDetailView.as_view(), name="detail"),
]
