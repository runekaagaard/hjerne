from django.core.management.base import BaseCommand, CommandError
from context.models import ChangeSet, Context

class Command(BaseCommand):
    help = 'Remove a context from a changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('symbol_name', type=str, help='The name of the symbol to remove')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']
        symbol_name = kwargs['symbol_name']

        try:
            changeset = ChangeSet.objects.get(id=changeset_id)
        except ChangeSet.DoesNotExist:
            raise CommandError('ChangeSet "%s" does not exist' % changeset_id)

        try:
            context = Context.objects.get(change_set=changeset, symbol=symbol_name)
            context.delete()
            self.stdout.write(self.style.SUCCESS('Successfully removed context for symbol "%s" from changeset "%s"' % (symbol_name, changeset_id)))
        except Context.DoesNotExist:
            raise CommandError('Context for symbol "%s" does not exist in changeset "%s"' % (symbol_name, changeset_id))
from django.core.management.base import BaseCommand, CommandError
from context.models import ChangeSet, Context

class Command(BaseCommand):
    help = 'Remove a context from a changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('symbol_name', type=str, help='The name of the symbol to remove')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']
        symbol_name = kwargs['symbol_name']

        try:
            changeset = ChangeSet.objects.get(id=changeset_id)
        except ChangeSet.DoesNotExist:
            raise CommandError('ChangeSet "%s" does not exist' % changeset_id)

        try:
            context = Context.objects.get(change_set=changeset, symbol=symbol_name)
            context.delete()
            self.stdout.write(self.style.SUCCESS('Successfully removed context for symbol "%s" from changeset "%s"' % (symbol_name, changeset_id)))
        except Context.DoesNotExist:
            raise CommandError('Context for symbol "%s" does not exist in changeset "%s"' % (symbol_name, changeset_id))
