from django.urls import path

from .views import LandingView, StatusView,AboutView,DashboardPreviewView


app_name = "workspaces"


urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("status/", StatusView.as_view(), name="status"),
    path("about/", AboutView.as_view(), name="about"),
    path("dashboard/", DashboardPreviewView.as_view(), name="dashboard"),
]