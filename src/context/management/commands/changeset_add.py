from django.core.management.base import BaseCommand, CommandError
from context.models import Project, Changeset

class Command(BaseCommand):
    help = 'Add a changeset to a project'

    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int, help='The ID of the project')
        parser.add_argument('title', type=str, help='The title of the changeset')

    def handle(self, *args, **kwargs):
        project_id = kwargs['project_id']
        title = kwargs['title']

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise CommandError('Project "%s" does not exist' % project_id)

        changeset = Changeset.objects.create(project=project, title=title)
        self.stdout.write(self.style.SUCCESS('Successfully added changeset "%s" to project "%s" with ID %d' % (title, project.title, changeset.id)))
