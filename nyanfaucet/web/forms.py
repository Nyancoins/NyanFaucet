from django import forms

from cryptocoin.rpc import get_faucet_balance
from cryptocoin.validation import validate_nyan
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
    remember_me = forms.BooleanField(required=False, initial=True)

class RegisterForm(forms.ModelForm):
    remember_me = forms.BooleanField(required=False, initial=True)

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

class WithdrawForm(forms.Form):
    amount = forms.FloatField()

    def __init__(self, usr, *args, **kwargs):
        super(WithdrawForm, self).__init__(*args, **kwargs)
        self.usr = usr

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 10:
            raise forms.ValidationError("You need to withdraw at least 10 NYAN.")
        if amount > self.usr.balance:
            raise forms.ValidationError("You cannot withdraw more than you have!")
        
        return amount

    def clean(self):
        data = super(WithdrawForm, self).clean()

        balance = get_faucet_balance()
        if balance is not None and balance <= data.get('amount'):
            raise forms.ValidationError("Well this is embarassing... the faucet does not have enough coins to process your withdrawal.")
    
