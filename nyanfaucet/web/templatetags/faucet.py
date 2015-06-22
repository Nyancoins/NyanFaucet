from django import template
from django.core.urlresolvers import reverse
from django.core.cache import get_cache
from django.contrib.humanize.templatetags.humanize import intcomma

from web.models import FaucetUser
from cryptocoin.rpc import get_faucet_balance

register = template.Library()

@register.simple_tag
def balance(request):
    if 'address' not in request.session:
        return 'error'

    usr = FaucetUser.find_by_address(request.session['address'])
    if usr is None:
        return 'error'

    return usr.balance

@register.simple_tag
def faucet_balance():
    c = get_cache('default')
    details = None
    b = c.get('faucet_balance', None)
    if b is None:
        b, details = get_faucet_balance()
        c.set('faucet_balance', (b, details), 60)
    else:
        b, details = b

    return intcomma(b)
