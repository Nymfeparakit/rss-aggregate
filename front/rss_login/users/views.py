from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "login_user.html"

    def post(self):
