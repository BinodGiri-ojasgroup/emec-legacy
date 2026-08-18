from django.urls import path

from apps.projects.views import ProjectDetailView, ProjectListView

app_name = "projects"

urlpatterns = [
    path("", ProjectListView.as_view(), name="index"),
    path("<slug:slug>/", ProjectDetailView.as_view(), name="detail"),
]
