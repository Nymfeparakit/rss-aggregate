from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
]
