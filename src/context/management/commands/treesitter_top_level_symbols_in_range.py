# This command is for debug usage only

from django.core.management.base import BaseCommand, CommandError
from context.api import init_file, top_level_symbols_in_range

class Command(BaseCommand):
    help = 'Output top-level symbols in a given range for a given file using Tree-sitter'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the file')
        parser.add_argument('row_from', type=int, help='The starting row number')
        parser.add_argument('row_to', type=int, help='The ending row number')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        row_from = kwargs['row_from']
        row_to = kwargs['row_to']

        try:
            symbols = top_level_symbols_in_range(file_path, row_from, row_to)
        except Exception as e:
            raise CommandError(f"Error finding top-level symbols: {e}")

        self.stdout.write(f"Top-level symbols in {file_path} from row {row_from} to {row_to}:\n")
        for symbol in symbols:
            node = symbol['node']
            symbol_name = symbol['symbol_name']
            start_line, start_col = node.start_point
            end_line, end_col = node.end_point
            self.stdout.write(f"Symbol: {symbol_name}\n")
            self.stdout.write(f"  Start: Line {start_line + 1}, Column {start_col + 1}\n")
            self.stdout.write(f"  End: Line {end_line + 1}, Column {end_col + 1}\n")
            self.stdout.write("\n")
