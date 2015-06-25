from django import template
from django.core.urlresolvers import reverse

from web.models import FaucetUser

register = template.Library()

@register.inclusion_tag('account_rolls.html')
def list_rolls(rolls):
    return { 'rolls': rolls }

@register.inclusion_tag('account_withdrawals.html')
def list_withdrawals(withdrawals):
    return { 'withdrawals': withdrawals }

@register.simple_tag
def balance(request):
    if 'address' not in request.session:
        return 'error'

    usr = FaucetUser.find_by_address(request.session['address'])
    if usr is None:
        return 'error'

    return usr.balance

@register.filter('number2words')
def number2words(num):
    from num2words import num2words
    return num2words(num)