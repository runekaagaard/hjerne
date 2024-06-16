from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Context

class Command(BaseCommand):
    help = 'Clear all contexts in a changeset'

    def add_arguments(self, parser):
        parser.add_argument('changeset_id', type=int, help='The ID of the changeset')

    def handle(self, *args, **kwargs):
        changeset_id = kwargs['changeset_id']

        try:
            changeset = Changeset.objects.get(id=changeset_id)
        except Changeset.DoesNotExist:
            raise CommandError('Changeset "%s" does not exist' % changeset_id)

        Context.objects.filter(changeset=changeset).delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all contexts in changeset "%s"' % changeset_id))
