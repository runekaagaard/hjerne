from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Changeset, Context

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

class ContextInline(admin.TabularInline):
    model = Context
    extra = 1

@admin.register(Changeset)
class ChangesetAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'description')
    search_fields = ('title', 'project__title', 'description')
    list_filter = ('project',)
    inlines = [ContextInline]

@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'file', 'changeset')
    search_fields = ('symbol', 'file', 'changeset__title')
    list_filter = ('changeset',)
