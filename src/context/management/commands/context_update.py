from django.core.management.base import BaseCommand, CommandError
from context.models import ChangeSet, Context
from context.api import update_file

class Command(BaseCommand):
    help = 'Update a context with the given replacement file'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')
        parser.add_argument('replacement_file', type=str, help='The path to the replacement file')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']
        replacement_file = kwargs['replacement_file']

        try:
            changeset = ChangeSet.objects.get(id=changeset_id)
        except ChangeSet.DoesNotExist:
            raise CommandError('ChangeSet "%s" does not exist' % changeset_id)

        contexts = Context.objects.filter(change_set=changeset)
        if not contexts:
            raise CommandError('No contexts found for changeset "%s"' % changeset_id)

        context = None
        if len(contexts) > 1:
            self.stdout.write(self.style.WARNING('The symbol exists in multiple files.'))
            for i, ctx in enumerate(contexts):
                self.stdout.write(f"{i + 1}. {ctx.file}")
            choice = int(input("Enter the number of the file you want to update: ")) - 1
            context = contexts[choice]
        else:
            context = contexts[0]
        if len(contexts) > 1:
            self.stdout.write(self.style.WARNING('The symbol exists in multiple files.'))
            for i, ctx in enumerate(contexts):
                self.stdout.write(f"{i + 1}. {ctx.file}")
            choice = int(input("Enter the number of the file you want to update: ")) - 1
            context = contexts[choice]

        update_file(context.file, replacement_file, context.file)
        self.stdout.write(self.style.SUCCESS('Successfully updated context "%s"' % changeset_id))
