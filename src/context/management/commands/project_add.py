from django.core.management.base import BaseCommand, CommandError
from context.models import Project

class Command(BaseCommand):
    help = 'Add a project'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='The title of the project')
        parser.add_argument('description', type=str, help='The description of the project')

    def handle(self, *args, **kwargs):
        title = kwargs['title']
        description = kwargs['description']

        project = Project.objects.create(title=title, description=description)
        self.stdout.write(self.style.SUCCESS(f'Successfully added project "{title}" with ID {project.id}'))
