from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

class BaseModel(models.Model):
  created_date = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True


class FaucetUser(BaseModel):
  address = models.CharField(max_length=48, unique=True)
  email = models.EmailField(unique=True) # @todo: for verification?
  last_roll = models.DateTimeField(auto_now=True)
  balance = models.PositiveIntegerField(default=0)

  def __unicode__(self):
      return self.email

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

class Withdrawal(BaseModel):
  # Model for storing withdrawals for each FaucetUser
  amount = models.PositiveIntegerField()
  transaction = models.CharField(max_length=64)
  user = models.ForeignKey(FaucetUser, related_name='withdrawals')

  class Meta:
    verbose_name_plural = "Withdrawals"
