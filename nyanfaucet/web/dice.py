import hmac
import math
import os

SERVER_IDENT = "nyan~ :3!"  # used for server seed
DIVIDER = 429496.7295       # based on the FreeDogecoin formula, for normalizing values between 0 and 10.000 (? @todo: check! )

WINNINGS_MULTIPLIERS = {
    10000: 1,       # 1 in 10.000       00.01 %
    9998: 0.1,      # 2 in 10.000       00.02 %
    9994: 0.001,    # 4 in 10.000       00.04 %
    9986: 0.0001,   # 8 in 10.000       00.08 %
    0: 0.00001,     # 9985 in 10.000    99.85 %
}
"""
    Descending list of multipliers.
"""

def CalculateWinnings(value, prize):
    """
        Calculate payouts for dice roll using a descending multiplier slide (WINNINGS_MULTIPLIERS needs to be sorted in descending order).

        value -- the dice roll
        prize -- max. winnable amount (jackpot) and base for multipliers
    """
    multi = 0
    for v in sorted(WINNINGS_MULTIPLIERS.iterkeys(), reverse=True):
        if value >= v:
            multi = WINNINGS_MULTIPLIERS[v]
            break
    if multi == 0:
        raise Exception("Multiplier not supposed to be 0 (zero)")

    win = prize * multi
    return win

def RollDice(nonce, clientseed):
    """
        Let's roll the dice like FreeDogecoin (see https://freedoge.co.in)

        nonce -- should be different for each roll, by default: total number of rolls user has made
        clientseed -- Seed set by JavaScript in client browser (CSRF warning!)

        Returns tuple (roll, generated_server_seed)
    """
    server_seed = "%s:%s:%s" % (os.urandom(8).encode('base64'), SERVER_IDENT, os.urandom(8).encode('base64'))
    in1 = "%d:%s:%d" % (nonce, server_seed, nonce)
    in2 = "%d:%s:%d" % (nonce, clientseed, nonce)
    
    h = hmac.new(in1)
    h.update(in2)
    hex = h.hexdigest()
    
    slice = float(int(hex[:8], 16))
    roll = int(math.ceil(slice / DIVIDER))
    return roll, server_seed.decode('utf8')
