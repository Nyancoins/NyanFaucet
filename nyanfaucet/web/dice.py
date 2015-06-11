import hmac
import math
import os

SERVER_IDENT = "nyan~ :3!"
DIVIDER = 429496.7295

def RollDice(nonce, clientseed):
    server_seed = "%s:%s:%s" % (os.urandom(8).encode('base64'), SERVER_IDENT, os.urandom(8).encode('base64'))
    in1 = "%d:%s:%d" % (nonce, server_seed, nonce)
    in2 = "%d:%s:%d" % (nonce, clientseed, nonce)
    
    h = hmac.new(in1)
    h.update(in2)
    hex = h.hexdigest()
    
    slice = float(int(hex[:8], 16))
    roll = int(math.ceil(slice / DIVIDER))
    return roll, server_seed.decode('utf8')
