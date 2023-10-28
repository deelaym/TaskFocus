from django.shortcuts import render
from .models import Project, Day, Task


def index(request):
    initialize()
    projects = Project.objects.all()
    return render(request, 'index.html', {'projects': projects})

def initialize():
    if Project.objects.all().count() == 0:
        python = Project.objects.create(name='Python')
        sport = Project.objects.create(name='Sport')
        day1 = Day.objects.create(project=python, name='Day1')
        day2 = Day.objects.create(project=python, name='Day2')
        Task.objects.bulk_create([
            Task(day=day1, name='Learn basics'),
            Task(day=day1, name='Learn loops'),
            Task(day=day1, name='Something'),
        ])
        Task.objects.bulk_create([
            Task(day=day2, name='Learn conditions'),
            Task(day=day2, name='Solve problems'),
            Task(day=day2, name='Something more'),
        ])
