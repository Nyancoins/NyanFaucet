from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required

from web.forms import LoginForm

# Create your views here.

class DefaultView(generic.TemplateView):
	template_name = "default.html"

class LoginView(generic.FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/play/"