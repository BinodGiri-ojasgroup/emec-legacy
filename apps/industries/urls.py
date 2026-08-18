from django.urls import path

from apps.industries.views import IndustryDetailView, IndustryListView

app_name = "industries"

urlpatterns = [
    path("", IndustryListView.as_view(), name="index"),
    path("<slug:slug>/", IndustryDetailView.as_view(), name="detail"),
]
