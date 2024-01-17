import requests
from django.conf import settings
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class SettingsView(TemplateView):
    SOURCES_URL = "sources"
    template_name = "settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TODO: use login to make authorization
        token = "123"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(f"{settings.BACKEND_BASE_URL}{self.SOURCES_URL}", headers=headers)
        sources = resp.json()
        # TODO: add DTO for sources
        context["sources"] = sources
        return context
