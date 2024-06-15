from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, ChangeSet, Context

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

@admin.register(ChangeSet)
class ChangeSetAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'description')
    search_fields = ('title', 'project__title', 'description')
    list_filter = ('project',)

@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'file', 'change_set')
    search_fields = ('symbol', 'file', 'change_set__title')
    list_filter = ('change_set',)
