from django import forms

# Helper functions #

# Lifesaver: http://stackoverflow.com/a/24003126
def to_bytes(n, length):
    return bytes( (n >> i*8) & 0xff for i in reversed(range(length)))

# Thanks http://rosettacode.org/wiki/Bitcoin/address_validation#Python
from hashlib import sha256
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return to_bytes(n, length)

def check_bc(bc):
    # @todo: Doesn't work. ._.
    bcbytes = decode_base58(bc, 25)
    return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]

# Validators #

class BitcoinAddress(forms.Field):
    def validate(self, value):
        return super(BitcoinAddress, self).validate(value)
        


# Forms #

class LoginForm(forms.Form):
    address = forms.CharField(required=True)
