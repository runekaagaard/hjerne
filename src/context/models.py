from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title", help_text="Enter the project title")
    description = models.TextField(verbose_name="Description", help_text="Enter the project description")

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title


class ChangeSet(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="Project", help_text="Select the project")
    title = models.CharField(max_length=200, verbose_name="Title", help_text="Enter the changeset title")
    description = models.TextField(blank=True, null=True, verbose_name="Description", help_text="Enter the changeset description (optional)")

    class Meta:
        verbose_name = "ChangeSet"
        verbose_name_plural = "ChangeSets"

    def __str__(self):
        return self.title


class Context(models.Model):
    change_set = models.ForeignKey(ChangeSet, on_delete=models.CASCADE, verbose_name="ChangeSet", help_text="Select the changeset")
    file = models.CharField(max_length=200, verbose_name="File", help_text="Enter the file name")
    symbol = models.CharField(max_length=200, verbose_name="Symbol", help_text="Enter the symbol name")

    class Meta:
        verbose_name = "Context"
        verbose_name_plural = "Contexts"

    
    class Meta:
        unique_together = ('change_set', 'file', 'symbol')
