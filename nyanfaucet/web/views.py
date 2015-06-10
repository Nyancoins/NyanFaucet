from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from web.forms import LoginForm, RegisterForm
from web.models import FaucetUser

# Create your views here.

class DefaultView(generic.TemplateView):
	template_name = "default.html"

class LoginView(generic.FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/play"

    def form_valid(self, form):
        addr = form.cleaned_data['address']

        usr = None
        try:
            usr = FaucetUser.objects.get(address=addr)
        except ObjectDoesNotExist:
            usr = None

        if usr is None:
            # @todo: Transparently create account? Redirect to signup?
            messages.error(self.request, "Account not found! Please double check the address or sign up for a new account.", 'danger')
            return redirect('login')

        self.request.session['address'] = addr
        return super(LoginView, self).form_valid(form)

class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "/play"

    def form_valid(self, form):
        addr = form.cleaned_data['address']
        email = form.cleaned_data['email']

        usr = FaucetUser(address=addr, email=email)
        usr.save()

        return redirect('register')

        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(RegisterView, self).get_context_data(**kwargs)
        return ctx

class LogoutView(generic.View):
    def get(self, request):
        request.session.flush()
        return redirect('default')
