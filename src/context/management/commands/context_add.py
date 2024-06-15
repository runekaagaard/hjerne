from django.core.management.base import BaseCommand, CommandError
from context.models import ChangeSet, Context
from context.api import top_level_symbol_at

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
            changeset = ChangeSet.objects.get(id=changeset_id)
        except ChangeSet.DoesNotExist:
            raise CommandError('ChangeSet "%s" does not exist' % changeset_id)

        symbol_name = top_level_symbol_at(filename, linenumber)["symbol_name"]
        _, created = Context.objects.get_or_create(change_set=changeset, file=filename, symbol=symbol_name)
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully added context to changeset "%s"' % changeset_id))
        else:
            self.stdout.write(self.style.WARNING('Context already exists for changeset "%s"' % changeset_id))