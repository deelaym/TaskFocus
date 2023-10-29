from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Day, Task
from .forms import DayForm, TaskForm



def index(request):
    initialize()
    projects = Project.objects.all()
    return render(request, 'index.html', {'projects': projects})


def project_detail(request, slug):
    project = Project.objects.get(slug=slug)
    form = DayForm()
    return render(request, 'project/detail.html', {'project': project,
                                                   'form': form})


def day_form(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        form = DayForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            day = Day(name=name, project=project)
            day.save()
            return redirect('project:project_detail', slug=slug)
    else:
        form = DayForm()
        return render(request, 'includes/day/create.html', {'form': form, 'project': project})


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
