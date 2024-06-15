from django.core.management.base import BaseCommand, CommandError
from context.models import ChangeSet, Context
from context.api import code_for_context

class Command(BaseCommand):
    help = 'Output code for a given changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']

        try:
            changeset = ChangeSet.objects.get(id=changeset_id)
        except ChangeSet.DoesNotExist:
            raise CommandError('ChangeSet "%s" does not exist' % changeset_id)

        contexts = Context.objects.filter(change_set=changeset)
        contexts_by_file = {}
        for context in contexts:
            if context.file not in contexts_by_file:
                contexts_by_file[context.file] = []
            contexts_by_file[context.file].append(context)

        for i, (file, contexts) in enumerate(contexts_by_file.items()):
            if i:
                self.stdout.write("\n")
            self.stdout.write(f"# file: {file}\n")
            self.stdout.write("```python")
            for j, context in enumerate(contexts):
                if j:
                    self.stdout.write("\n")
                code = code_for_context(context)
                self.stdout.write(code)
            self.stdout.write("```\n")
