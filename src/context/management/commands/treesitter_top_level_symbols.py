# This command is for debug usage only

from django.core.management.base import BaseCommand, CommandError
from context.api import init_file, top_level_symbols

class Command(BaseCommand):
    help = 'Output top-level symbols for a given file using Tree-sitter'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        try:
            _, tree, query = init_file(file_path)
        except Exception as e:
            raise CommandError(f"Error initializing file: {e}")

        self.stdout.write(f"Top-level symbols in {file_path}:\n")
        for symbol in top_level_symbols(tree, query):
            node = symbol['node']
            symbol_name = symbol['symbol_name']
            start_line, start_col = node.start_point
            end_line, end_col = node.end_point
            self.stdout.write(f"Symbol: {symbol_name}\n")
            self.stdout.write(f"  Start: Line {start_line + 1}, Column {start_col + 1}\n")
            self.stdout.write(f"  End: Line {end_line + 1}, Column {end_col + 1}\n")
            self.stdout.write("\n")
