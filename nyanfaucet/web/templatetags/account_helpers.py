from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('account_rolls.html')
def list_rolls(rolls):
    return { 'rolls': rolls }

@register.inclusion_tag('account_withdrawals.html')
def list_withdrawals(withdrawals):
    return { 'withdrawals': withdrawals }