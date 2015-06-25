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
        b = None
        try:
            b = get_faucet_balance()
        except Exception as ex:
            print ex

        if b is None:
            b = "[RPC Error]"

        c.set('faucet_balance', b, 60)

    return intcomma(b)
