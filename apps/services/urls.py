from django.urls import path

from apps.services.views import ServiceDetailView, ServiceListView

app_name = "services"

urlpatterns = [
    path("", ServiceListView.as_view(), name="index"),
    path("<slug:slug>/", ServiceDetailView.as_view(), name="detail"),
]
