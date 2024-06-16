from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Context
from context.api import code_for_context

class Command(BaseCommand):
    help = 'Output code for a given changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']

        try:
            changeset = Changeset.objects.get(id=changeset_id)
        except Changeset.DoesNotExist:
            raise CommandError('Changeset "%s" does not exist' % changeset_id)

        contexts = Context.objects.filter(changeset=changeset)
        contexts_by_file = {}
        for context in contexts:
            if context.file not in contexts_by_file:
                contexts_by_file[context.file] = []
            contexts_by_file[context.file].append(context)

        for i, (file, contexts) in enumerate(contexts_by_file.items()):
            if i:
                self.stdout.write("\n")
            self.stdout.write(f"# file: {file}\n")
            for j, context in enumerate(contexts):
                if j:
                    self.stdout.write("\n")
                code = code_for_context(context)
                self.stdout.write(code)
            self.stdout.write("\n")
