from django.shortcuts import render, redirect
from django.views import generic
#from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse

from datetime import datetime, timedelta
from django.utils.timezone import utc

from web.forms import LoginForm, RegisterForm, RollForm, WithdrawForm
from web.models import FaucetUser, Roll, Withdrawal

from dice import RollDice, CalculateWinnings, WINNINGS_MULTIPLIERS
from cryptocoin.rpc import send as send_nyan
from cryptocoin.rpc import get_faucet_balance
from django.core.mail import send_mail
from django.utils.safestring import SafeString
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from nyanfaucet.strings import ACCOUNT_DISABLED, INVALID_SESSION, LOGIN_REQUIRED, ACCOUNT_NOT_FOUND, ACCOUNT_CONFIRMATION_SENT, ACCOUNT_ALREADY_ACTIVATED, INVALID_ACTIVATION_LINK, SAFE_ACCOUNT_NOT_YET_CONFIRMED, DICE_ALREADY_ROLLED, WITHDRAWAL_FAILED, ACCOUNT_ACTIVATED

jackpot = settings.NYAN_JACKPOT # @todo set dynamically to some cash value

# Create your views here.

import urllib
def nyan_login_required(function=None):
    def wrapper(request, *args, **kwargs):
        s = request.session
        if 'address' not in s:
            messages.warning(request, LOGIN_REQUIRED)
            s['return'] = request.get_full_path()
            return redirect('login')
        else:
            try:
                usr = FaucetUser.objects.get(address=s['address'])
                if usr.enabled == False:
                    s.flush()
                    messages.warning(request, ACCOUNT_DISABLED)
                    return redirect('default')
                
                if not usr.email_confirmed:
                    messages.warning(request, SafeString(SAFE_ACCOUNT_NOT_YET_CONFIRMED % (reverse('activation_helper'))))
            except ObjectDoesNotExist:
                usr = None
                messages.warning(request, INVALID_SESSION, 'danger')
                s.flush()
                s['return'] = request.get_full_path()
                return redirect('login')

        return function(request, *args, **kwargs)
    return wrapper

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class NyanFaucetMixin(object):
    def get_context_data(self, **kwargs):
        context = super(NyanFaucetMixin, self).get_context_data(**kwargs)

        context['faucetbalance'] = get_faucet_balance() or SafeString("<strong>Unavailable</strong> <i>(RPC failure)</i>")
        context['faucetminbalance'] = settings.NYAN_MINBALANCE
        context['balance'] = FaucetUser.objects.get(address=self.request.session['address']).balance

        return context
       

class DefaultView(NyanFaucetMixin, generic.TemplateView):
	template_name = "default.html"

class LoginView(generic.FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/play"

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if remember_me:
            self.request.session.set_expiry(None)
        else:
            self.request.session.set_expiry(0)

        addr = form.cleaned_data['address']
        usr = None
        try:
            usr = FaucetUser.objects.get(address=addr)
        except ObjectDoesNotExist:
            usr = None

        if usr is None:
            # @todo: Transparently create account?
            self.request.session.flush()
            messages.error(self.request, ACCOUNT_NOT_FOUND, 'danger')
            return redirect('login')
        
        usr.update_balance()
        self.request.session['address'] = addr

        ret = self.request.session.pop('return', None)
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

        remember_me = form.cleaned_data['remember_me']
        if remember_me:
            self.request.session.set_expiry(None)
        else:
            self.request.session.set_expiry(0)

        usr = FaucetUser(address=addr, email=email, email_confirmed=False)
        usr.save()
        usr.send_reg_confirm_mail()

        messages.info(self.request, ACCOUNT_CONFIRMATION_SENT)
        self.request.session['address'] = addr

        return super(RegisterView, self).form_valid(form)

class LogoutView(generic.View):
    def get(self, request):
        request.session.flush()
        return redirect('default')

class ActivationHelper(generic.View):

    @method_decorator(nyan_login_required)
    def dispatch(self, *args, **kwargs):
        usr = FaucetUser.objects.get(address=self.request.session['address'])

        if usr is not None:
            if usr.email_confirmed is True:
                messages.info(self.request, ACCOUNT_ALREADY_ACTIVATED)
            else:
                nonce = self.kwargs.get('nonce', None)
                if nonce is not None:
                    if nonce == usr.email_confirm_nonce:
                        usr.email_confirmed = True
                        usr.save()
                        messages.info(self.request, ACCOUNT_ACTIVATED)
                    else:
                        messages.error(self.request, INVALID_ACTIVATION_LINK, 'danger')
                        self.request.session.flush()
                        return HttpResponseRedirect(reverse('default'))
                else:
                    messages.info(self.request, ACCOUNT_CONFIRMATION_SENT)
                    usr.send_reg_confirm_mail()

        return reverse('play')


class PlayView(NyanFaucetMixin, AjaxableResponseMixin, generic.FormView):
    template_name = "play.html"
    form_class = RollForm
    success_url = "/play"

    @method_decorator(nyan_login_required)
    def dispatch(self, *args, **kwargs):
        return super(PlayView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        """
            GET & POST - template variables
        """
        ctx = super(PlayView, self).get_context_data(**kwargs)

        usr = FaucetUser.objects.get(address=self.request.session['address'])
        nonce = usr.rolls.count() +1
        

        if usr.rolls.count() > 0:
            nextroll = ((usr.last_roll - datetime.now(utc)) + timedelta(seconds=settings.NYAN_ROLL_INTERVAL)).total_seconds()
            lr = usr.rolls.last()
            ctx['nextroll'] = nextroll
            ctx['lastroll'] = lr.value
            ctx['lastwinnings'] = lr.winnings
        else:
            ctx['nextroll'] = 0

        ctx['nonce'] = nonce
        ctx['jackpot'] = jackpot

        payout_table = []
        for v in sorted(WINNINGS_MULTIPLIERS.iterkeys(), reverse=False):
            payout_table.append([v, jackpot*WINNINGS_MULTIPLIERS[v]])
        ctx['payout_table'] = payout_table
        
        return ctx

    def form_valid(self, form):
        """
            POST - roll dice from user input
        """
        cs = form.cleaned_data['seed']

        usr = FaucetUser.objects.get(address=self.request.session['address'])
        
        if usr.rolls.count() > 0:
            nextroll = ((usr.last_roll - datetime.utcnow().replace(tzinfo=utc)) + timedelta(seconds=settings.NYAN_ROLL_INTERVAL)).total_seconds()
            if nextroll >= 0:
                return HttpResponseForbidden(DICE_ALREADY_ROLLED)

        # Roll dice
        nonce = usr.rolls.count() +1
        diceroll, ss = RollDice(nonce, cs)

        winnings = CalculateWinnings(diceroll, jackpot)

        r = Roll(user=usr, value=diceroll, clientseed=cs, serverseed=ss, nonce=nonce, winnings=winnings)
        r.save()
        usr.save()

        return super(PlayView, self).form_valid(form)

class HistoryView(generic.TemplateView):
    template_name = "history.html"

    @method_decorator(nyan_login_required)
    def dispatch(self, *args, **kwargs):
        return super(HistoryView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)

        usr = FaucetUser.objects.get(address=self.request.session['address'])

        context['withdrawals'] = usr.withdrawals.order_by('-pk').all()[:30]
        context['rolls'] = usr.rolls.order_by('-pk').all()[:30]
        return context

class WithdrawView(NyanFaucetMixin, generic.FormView):
    template_name = "withdraw.html"
    form_class = WithdrawForm
    success_url = '/withdraw'

    @method_decorator(nyan_login_required)
    def dispatch(self, *args, **kwargs):        
        return super(WithdrawView, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        """
        This is needed for form validation (?)
        """
        kwargs = super(WithdrawView, self).get_form_kwargs()
        kwargs.update({
            'usr': FaucetUser.objects.get(address=self.request.session['address']),
        })
        return kwargs

    def form_valid(self, form, **kwargs):
        c = self.get_context_data(**kwargs)
        c['withdrawal_ok'] = True
        c['form'] = form

        amount = form.cleaned_data['amount']

        usr = FaucetUser.objects.get(address=self.request.session['address'])

        tx = send_nyan(usr.address, amount)
        if tx is None:
            messages.error(self.request, WITHDRAWAL_FAILED, 'danger')
            c['withdrawal_ok'] = False
            return self.render_to_response(c, **kwargs)
        else:
            w = Withdrawal(user=usr, transaction=tx, amount=amount)
            w.save()

        return self.render_to_response(c, **kwargs)


