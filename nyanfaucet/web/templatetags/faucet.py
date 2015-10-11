from django import template
from django.core.urlresolvers import reverse
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.safestring import SafeString

from cryptocoin.rpc import get_faucet_balance

register = template.Library()

@register.simple_tag
def faucet_balance():
    b = get_faucet_balance()

    if b is None:
        return SafeString("<strong>Unavailable</strong> <i>(RPC failure)</i>")

    return intcomma(b) + " NYAN"
