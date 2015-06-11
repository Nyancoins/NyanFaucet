from django.contrib import admin

from web.models import FaucetUser, Roll, Withdrawal

# Register your models here.

@admin.register(FaucetUser)
class FaucetUserAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'email', 'address', 'last_roll')

@admin.register(Roll)
class RollAdmin(admin.ModelAdmin):
    list_display = ('created_date', 'user', 'value')
    list_filter = ('user',)

admin.site.register(Withdrawal)
