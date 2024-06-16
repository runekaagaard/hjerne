from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Context
from context.api import top_level_symbols_in_range

class Command(BaseCommand):
    help = 'Add a context to a changeset'

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

        symbols = top_level_symbols_in_range(filename, linenumber, linenumber)
        if not symbols:
            raise CommandError(f"No top level symbol found in {filename} at line {linenumber}.")
        symbol_name = symbols[0]["symbol_name"]
        _, created = Context.objects.get_or_create(changeset=changeset, file=filename, symbol=symbol_name)
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully added context to changeset "%s"' % changeset_id))
        else:
            self.stdout.write(self.style.WARNING('Context already exists for changeset "%s"' % changeset_id))
