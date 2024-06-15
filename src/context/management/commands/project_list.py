from django.core.management.base import BaseCommand
from context.models import Project

class Command(BaseCommand):
    help = 'List all projects with their IDs and titles'

    def handle(self, *args, **kwargs):
        projects = Project.objects.all()
        for project in projects:
            self.stdout.write(f"{project.id} {project.title}")
