from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Context
from context.api import init_files_from_markdown, update_symbol

class Command(BaseCommand):
    help = 'Update the context for a given changeset using a markdown file'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('markdown_file', type=str, help='The path to the markdown file')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']
        markdown_file = kwargs['markdown_file']

        try:
            changeset = Changeset.objects.get(id=changeset_id)
        except Changeset.DoesNotExist:
            raise CommandError('Changeset "%s" does not exist' % changeset_id)

        contexts = Context.objects.filter(changeset=changeset)
        file_data = init_files_from_markdown(markdown_file)

        for context in contexts:
            for filename, language_name, parser, tree, query in file_data:
                if context.file == filename:
                    replacement_symbols = {
                        symbol['symbol_name']: symbol['node'].text.decode() for symbol in top_level_symbols(tree, query)
                    }

                    if context.symbol in replacement_symbols:
                        update_symbol(context.file, context.symbol, replacement_symbols[context.symbol])
                        self.stdout.write(self.style.SUCCESS(f"Symbol '{context.symbol}' updated in file '{context.file}'!"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Symbol '{context.symbol}' not found in file '{context.file}'"))

        self.stdout.write(self.style.SUCCESS('Successfully updated context for changeset "%s"' % changeset_id))
