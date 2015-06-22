from django import forms

from web.btc import validate_nyan
from web.models import FaucetUser

class BtcAddressField(forms.CharField):
    def validate(self, value):
        valid = validate_nyan(value)
        if valid is False:
            raise forms.ValidationError("The address you have entered is NOT valid! A valid address looks like this: KQm7yxJ4EWoohRHv3NaSH8VMxT3owf1oWk")
        return super(BtcAddressField, self).validate(value)


# Forms

class LoginForm(forms.Form):
    address = BtcAddressField(required=True, label='NyanCoin Address')
    remember_me = forms.BooleanField(required=False, initial=False)

class RegisterForm(forms.ModelForm):
    remember_me = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = FaucetUser
        fields = ['address', 'email']

    def clean_address(self):
        addr = self.cleaned_data['address']
        if validate_nyan(addr) is False:
            raise forms.ValidationError("The address you have entered is NOT valid! A valid address looks like this: KQm7yxJ4EWoohRHv3NaSH8VMxT3owf1oWk")
        return addr

class RollForm(forms.Form):
    seed = forms.CharField(max_length=32)
    
