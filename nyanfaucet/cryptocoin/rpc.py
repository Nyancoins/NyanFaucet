import logging
import traceback
from django.conf import settings
from django.core.cache import caches
from bitcoinrpc.authproxy import AuthServiceProxy

log = logging.getLogger('django.request')

sp = AuthServiceProxy(settings.RPC_URL)

def get_faucet_balance(cached=True):
    if cached == False:
        return rpc_balance()

    cache = caches['default']
    b = cache.get('faucet_balance', None)
    if b is None:
        b = rpc_balance()
        if b is None:
            cache.set('faucet_balance', b, 10) # don't cache as long
        else:
            cache.set('faucet_balance', b, 60)
    return b

def rpc_balance():
    b = None
    try:
        b = sp.getbalance()
    except Exception as err:
        log.exception(err)

    """total = 0
    details = []
    for l in sp.listreceivedbyaddress():
        total += l['amount']
        details.append(dict(address=l['address'], amount=l['amount'], confirmations=l['confirmations']))

    return total, details"""

    return b

def send(addr, amount):
    tx = None
    try:
        balance = get_faucet_balance()
        if balance is not None and amount > balance:
            log.error("Tried to send %f but only have %f balance." % (amount, balance))
            return None
        tx = sp.sendtoaddress(addr, amount)
    except Exception as err:
        log.exception(err)
    return tx