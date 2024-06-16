from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand, CommandError
from context.models import Changeset, Project

class Command(BaseCommand):
    help = 'List all changesets with their IDs and titles'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int, help='The ID of the project')

    def handle(self, *args, **kwargs):
        project_id = kwargs['project_id']

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise CommandError('Project "%s" does not exist' % project_id)
        changesets = Changeset.objects.filter(project=project)
        for changeset in changesets:
            self.stdout.write(f"{changeset.id} {changeset.project.title}.{changeset.title}")
