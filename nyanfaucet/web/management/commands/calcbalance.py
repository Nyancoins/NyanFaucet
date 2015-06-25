from django.core.management.base import BaseCommand, CommandError

from web.models import FaucetUser

class Command(BaseCommand):
    help = 'Recalculate the active balance for every FaucetUser'

    def add_arguments(self, parser):
        parser.add_argument('--quiet', action='store_true', help='No output other than errors')

    def handle(self, *args, **options):
        for u in FaucetUser.objects.all():
            u.balance = u.calc_balance()
            if not options['quiet']:
                print "%s - %f NYAN" % (str(u), u.balance)
            u.save()
