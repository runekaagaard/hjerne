from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Context
from context.api import top_level_symbol_at

class Command(BaseCommand):
    help = 'Remove a context from a changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('filename', type=str, help='The name of the file')
        parser.add_argument('linenumber', type=int, help='The line number in the file')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']
        filename = kwargs['filename']
        linenumber = kwargs['linenumber']

        try:
            changeset = Changeset.objects.get(id=changeset_id)
        except Changeset.DoesNotExist:
            raise CommandError('Changeset "%s" does not exist' % changeset_id)

        symbol_name = top_level_symbol_at(filename, linenumber)["symbol_name"]
        try:
            context = Context.objects.get(changeset=changeset, file=filename, symbol=symbol_name)
            context.delete()
            self.stdout.write(
                self.style.SUCCESS('Successfully removed context for symbol "%s" from changeset %d' %
                                   (symbol_name, changeset_id)))
        except Context.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('Context for symbol "%s" does not exist in changeset %d' %
                                   (symbol_name, changeset_id)))
