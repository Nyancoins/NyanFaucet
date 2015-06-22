from django.core.management.base import BaseCommand, CommandError

from web.models import FaucetUser

class Command(BaseCommand):
    help = 'Recalculate the active balance for every FaucetUser'

    def add_arguments(self, parser):
        parser.add_argument('--quiet', action='store_true', help='No output other than errors')

    def handle(self, *args, **options):
        for u in FaucetUser.objects.all():
            balance = 0
            for r in u.rolls.all():
                balance += r.winnings

            for w in u.withdrawals.all():
                balance -= w.amount
                
            u.balance = balance
            if not options['quiet']:
                print "%s has a balance of %f NYAN" % (str(u), balance)
            u.save()
