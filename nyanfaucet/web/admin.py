from django.contrib import admin

from web.models import FaucetUser, Rolls, Withdrawals

# Register your models here.

admin.site.register(FaucetUser)
admin.site.register(Rolls)
admin.site.register(Withdrawals)
