from django.urls import path

from .views import LandingView, StatusView,AboutView


app_name = "workspaces"


urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("status/", StatusView.as_view(), name="status"),
    path("about/", AboutView.as_view(), name="about"),
]