from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from django.core.mail import send_mail

# Create your models here.

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FaucetUser(BaseModel):
    address = models.CharField(max_length=48, unique=True)
    email = models.EmailField(unique=True) # @todo: for verification?
    last_roll = models.DateTimeField(default=datetime.now() - timedelta(-1))
    balance = models.PositiveIntegerField(default=0)
    email_confirmed = models.BooleanField(default=True)

    def __unicode__(self):
        return self.email

    def calc_balance(self):
        b = 0
        for r in self.rolls.all():
            b += r.winnings
        for w in self.withdrawals.all():
            b -= w.amount
        return b

    def update_balance(self):
        b = 0
        for r in self.rolls.all():
            b += r.winnings
        for w in self.withdrawals.all():
            b -= w.amount
        if b != self.balance:
            self.balance = b
            self.save()

    def send_reg_confirm_mail(self):
        send_mail("Activate your NyanFaucet account", "Please confirm your registration by clicking this link: <link>", settings.SERVER_EMAIL, [self.email])
        # todo: make prettier, add link

    @staticmethod
    def find_by_address(addr):
        try:
            usr = FaucetUser.objects.get(address=addr)
            return usr
        except ObjectDoesNotExist:
            return None


class Roll(BaseModel):
    # Model for storing dice rolls for each FaucetUser
    value = models.PositiveIntegerField()
    user = models.ForeignKey(FaucetUser, related_name='rolls')
    serverseed = models.CharField(max_length=256)
    clientseed = models.CharField(max_length=32)
    nonce = models.PositiveIntegerField()
    winnings = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Rolls"

    def save(self, *args, **kwargs):
        super(Roll, self).save(*args, **kwargs)
        self.user.balance += self.winnings
        self.user.last_roll = datetime.now()
        self.user.save()

class Withdrawal(BaseModel):
    # Model for storing withdrawals for each FaucetUser
    amount = models.PositiveIntegerField()
    transaction = models.CharField(max_length=64)
    user = models.ForeignKey(FaucetUser, related_name='withdrawals')

    class Meta:
        verbose_name_plural = "Withdrawals"

    def save(self, *args, **kwargs):
        super(Withdrawal, self).save(*args, **kwargs)
        self.user.balance -= self.amount
        self.user.save()
