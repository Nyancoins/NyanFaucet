import logging
import traceback
from django.conf import settings
from bitcoinrpc.authproxy import AuthServiceProxy

log = logging.getLogger('django.request')

sp = AuthServiceProxy(settings.RPC_URL)

def get_faucet_balance():
    """total = 0
    details = []
    for l in sp.listreceivedbyaddress():
        total += l['amount']
        details.append(dict(address=l['address'], amount=l['amount'], confirmations=l['confirmations']))

    return total, details"""

    r = None
    try:
        r = sp.getbalance()
    except Exception as err:
        log.exception(err)
    return r

def send(addr, amount):
    tx = None
    try:
        tx = sp.sendtoaddress(addr, amount)
    except Exception as err:
        log.exception(err)
    return tx