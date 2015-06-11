from django.shortcuts import render, redirect
from django.views import generic
#from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseForbidden

from datetime import datetime, timedelta
from django.utils.timezone import utc

from web.forms import LoginForm, RegisterForm, RollForm
from web.models import FaucetUser, Roll

from dice import RollDice

# Create your views here.

import urllib
def nyan_login_required(function=None):
    def wrapper(request, *args, **kwargs):
        s = request.session
        if 'address' not in s:
            messages.warning(request, 'Please sign in first.', 'warning')
            s['return'] = request.get_full_path()
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrapper
       

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

        ret = self.request.session['return']
        if ret:
            return redirect(ret)

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

        self.request.session['address'] = addr

        return super(RegisterView, self).form_valid(form)

class LogoutView(generic.View):
    def get(self, request):
        request.session.flush()
        return redirect('default')

class PlayView(generic.FormView):
    template_name = "play.html"
    form_class = RollForm
    success_url = "/play"

    @method_decorator(nyan_login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlayView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PlayView, self).get_context_data(**kwargs)

        usr = FaucetUser.objects.get(address=self.request.session['address'])
        nonce = usr.rolls.count() +1

        if usr.rolls.count() > 0:
            nextroll = ((usr.last_roll - datetime.utcnow().replace(tzinfo=utc)) + timedelta(seconds=settings.NYAN_ROLL_INTERVAL)).total_seconds()
            ctx['nextroll'] = nextroll
            ctx['lastroll'] = usr.rolls.last().value

        ctx['nonce'] = nonce
        #print ctx['nextroll']
        return ctx

    def form_valid(self, form):
        cs = form.cleaned_data['seed']

        usr = FaucetUser.objects.get(address=self.request.session['address'])
        
        if usr.rolls.count() > 0:
            nextroll = ((usr.last_roll - datetime.utcnow().replace(tzinfo=utc)) + timedelta(seconds=settings.NYAN_ROLL_INTERVAL)).total_seconds()
            if nextroll >= 0:
                return HttpResponseForbidden("You already rolled the dice once this round!")

        # Roll dice
        nonce = usr.rolls.count() +1
        diceroll, ss = RollDice(nonce, cs)

        r = Roll(user=usr, value=diceroll, clientseed=cs, serverseed=ss, nonce=nonce)
        r.save()
        usr.save()

        return super(PlayView, self).form_valid(form)