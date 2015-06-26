from django import template
from django.core.urlresolvers import reverse
from django.core.cache import caches
from django.contrib.humanize.templatetags.humanize import intcomma

from cryptocoin.rpc import get_faucet_balance

register = template.Library()

@register.simple_tag
def faucet_balance():
    c = caches['default']
    b = c.get('faucet_balance', None)
    if b is None:
        b = get_faucet_balance()

        if b is None:
            return "Unavailable (RPC error)"

        c.set('faucet_balance', b, 60)

    return intcomma(b) + " NYAN"
