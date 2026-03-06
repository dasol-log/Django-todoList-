from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class SignupPageView(TemplateView):
    template_name = "accounts/signup.html"


class LoginPageView(TemplateView):
    template_name = "accounts/login.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("page-login")
