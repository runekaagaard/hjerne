
from django.core.management.base import BaseCommand, CommandError
from context.models import ChangeSet, Context
from context.api import update_symbol, code_for_context

class Command(BaseCommand):
    help = 'Update the context for a given changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('replacement_file', type=str, help='The path to the replacement file')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']

        try:
            changeset = ChangeSet.objects.get(id=changeset_id)
        except ChangeSet.DoesNotExist:
            raise CommandError('ChangeSet "%s" does not exist' % changeset_id)

        contexts = Context.objects.filter(change_set=changeset)
        replacement_file_path = kwargs['replacement_file']
        
        for context in contexts:
            source_file_path = context.file
            destination_file_path = context.file  # Update the same file

            replacement_code = code_for_context(context)
            update_symbol(source_file_path, context.symbol, replacement_code)
            source_file_path = context.file
            replacement_file_path = context.file  # Assuming the replacement code is in the same file
            destination_file_path = context.file  # Update the same file

            replacement_code = code_for_context(context)
            update_symbol(source_file_path, context.symbol, replacement_code)

        self.stdout.write(self.style.SUCCESS('Successfully updated context for changeset "%s"' % changeset_id))
