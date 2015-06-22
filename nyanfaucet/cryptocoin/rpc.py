from django.conf import settings
from bitcoinrpc.authproxy import AuthServiceProxy

sp = AuthServiceProxy(settings.RPC_URL)

def get_faucet_balance():
    total = 0
    details = []
    for l in sp.listreceivedbyaddress():
        total += l['amount']
        details.append(dict(address=l['address'], amount=l['amount'], confirmations=l['confirmations']))

    return total, details