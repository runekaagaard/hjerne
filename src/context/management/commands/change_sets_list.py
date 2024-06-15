from django.core.management.base import BaseCommand
from context.models import ChangeSet

class Command(BaseCommand):
    help = 'List all changesets with their IDs and titles'

    def handle(self, *args, **kwargs):
        changesets = ChangeSet.objects.all()
        for changeset in changesets:
            self.stdout.write(f"{changeset.id} {changeset.title}")
