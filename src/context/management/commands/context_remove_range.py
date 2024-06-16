from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Context
from context.api import top_level_symbols_in_range

class Command(BaseCommand):
    help = 'Remove contexts from a changeset for a given range of lines in a file'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('file_path', type=str, help='The path to the file')
        parser.add_argument('from_line', type=int, help='The starting line number')
        parser.add_argument('to_line', type=int, help='The ending line number')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']
        file_path = kwargs['file_path']
        from_line = kwargs['from_line']
        to_line = kwargs['to_line']

        try:
            changeset = Changeset.objects.get(id=changeset_id)
        except Changeset.DoesNotExist:
            raise CommandError('Changeset "%s" does not exist' % changeset_id)

        symbols = top_level_symbols_in_range(file_path, from_line, to_line)
        if not symbols:
            raise CommandError(f"No top level symbols found in {file_path} between lines {from_line} and {to_line}.")

        for symbol in symbols:
            symbol_name = symbol["symbol_name"]
            try:
                context = Context.objects.get(changeset=changeset, file=file_path, symbol=symbol_name)
                context.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully removed context for symbol "{symbol_name}" from changeset "{changeset_id}"'))
            except Context.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Context for symbol "{symbol_name}" does not exist in changeset "{changeset_id}"'))
