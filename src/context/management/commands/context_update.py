from django.core.management.base import BaseCommand, CommandError
from context.models import ChangeSet, Context
from context.api import update_symbol, init_file, top_level_symbols

class Command(BaseCommand):
    help = 'Update the context for a given changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('replacement_file', type=str, help='The path to the replacement file')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']
        from_markdown = kwargs['from_markdown']

        try:
            changeset = ChangeSet.objects.get(id=changeset_id)
        except ChangeSet.DoesNotExist:
            raise CommandError('ChangeSet "%s" does not exist' % changeset_id)

        contexts = Context.objects.filter(change_set=changeset)

        for context in contexts:
            from context.api import init_file, extract_code_from_markdown
            _, tree, query = init_file(kwargs['replacement_file'])
                if from_markdown:
                    replacement_symbols = extract_code_from_markdown(kwargs['replacement_file'])
                else:
                    replacement_symbols = {
                        symbol['symbol_name']: symbol['node'].text.decode() for symbol in top_level_symbols(tree, query)
                    }

            if context.symbol in replacement_symbols:
                update_symbol(context.file, context.symbol, replacement_symbols[context.symbol])
            else:
                raise CommandError(f"Symbol '{context.symbol}' not found in replacement file")

        self.stdout.write(self.style.SUCCESS('Successfully updated context for changeset "%s"' % changeset_id))
