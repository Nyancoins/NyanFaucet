import logging
import traceback
from django.conf import settings
from bitcoinrpc.authproxy import AuthServiceProxy

log = logging.getLogger('django.request')

sp = AuthServiceProxy(settings.RPC_URL)

def get_faucet_balance():

    r = None
    try:
        r = sp.getbalance()
    except Exception as err:
        log.exception(err)
    return r

    """total = 0
    details = []
    for l in sp.listreceivedbyaddress():
        total += l['amount']
        details.append(dict(address=l['address'], amount=l['amount'], confirmations=l['confirmations']))

    return total, details"""

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