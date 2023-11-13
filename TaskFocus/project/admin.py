from django.contrib import admin
from .models import Project, Day, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['color', 'name', 'user', 'timer', 'edit_mode', 'time_intervals']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'complete']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'day', 'optional', 'complete']

