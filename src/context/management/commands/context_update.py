from django.core.management.base import BaseCommand, CommandError
from context.models import Context
from context.api import update_file

class Command(BaseCommand):
    help = 'Update a context with the given replacement file'

    def add_arguments(self, parser):
        parser.add_argument('context_id', type=int, help='The ID of the context to update')
        parser.add_argument('replacement_file', type=str, help='The path to the replacement file')

    def handle(self, *args, **kwargs):
        context_id = kwargs['context_id']
        replacement_file = kwargs['replacement_file']

        try:
            context = Context.objects.get(id=context_id)
        except Context.DoesNotExist:
            raise CommandError('Context "%s" does not exist' % context_id)

        contexts = Context.objects.filter(symbol=context.symbol)
        if len(contexts) > 1:
            self.stdout.write(self.style.WARNING('The symbol exists in multiple files.'))
            for i, ctx in enumerate(contexts):
                self.stdout.write(f"{i + 1}. {ctx.file}")
            choice = int(input("Enter the number of the file you want to update: ")) - 1
            context = contexts[choice]

        update_file(context.file, replacement_file, context.file)
        self.stdout.write(self.style.SUCCESS('Successfully updated context "%s"' % context_id))
