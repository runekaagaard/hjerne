from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Context
from context.api import code_for_context
import mimetypes

class Command(BaseCommand):
    help = 'Output code for a given changeset in markdown format, grouped by language'

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

        self.stdout.write(
            f"# {changeset.project.id} {changeset.project.title} - {changeset.id} {changeset.title}\n")
        if changeset.description:
            self.stdout.write(f"{changeset.description}\n")

        files_by_language = {}
        for file, contexts in contexts_by_file.items():
            language = mimetypes.guess_type(file)[0].split("/")[-1].split("-")[-1]
            if language not in files_by_language:
                files_by_language[language] = []
            files_by_language[language].append((file, contexts))

        for language, files in files_by_language.items():
            for file, contexts in files:
                self.stdout.write(f"\n## file: {file}\n")
                self.stdout.write(f"```{language}\n")
                for i, context in enumerate(contexts):
                    if i:
                        self.stdout.write("\n")

                    code = code_for_context(context)
                    self.stdout.write(code)
                self.stdout.write(f"```\n")
