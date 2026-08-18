from django.urls import path

from apps.team.views import LeadershipListView, TeamMemberDetailView

app_name = "team"

urlpatterns = [
    path("", LeadershipListView.as_view(), name="index"),
    path("<slug:slug>/", TeamMemberDetailView.as_view(), name="detail"),
]
