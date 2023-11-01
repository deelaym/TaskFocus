from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Day, Task
from .forms import DayForm, TaskForm, ProjectForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse


def index(request):
    initialize()
    projects = Project.objects.all()
    return render(request, 'index.html', {'projects': projects})

def project_create(request):
    if request.POST:
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = Project(name=project_form.cleaned_data['name'])
            project.save()
            return redirect('project:project_detail', slug=project.slug)
    else:
        project_form = ProjectForm()
        return render(request, 'project/create.html', {'project_form': project_form})


def project_delete(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()
    return redirect('project:index')

def pagination(request, slug):
    project = get_object_or_404(Project, slug=slug)
    day_list = project.days.all()
    paginator = Paginator(day_list, 1)
    page_number = request.GET.get('page', 1)
    try:
        days = paginator.page(page_number)
    except PageNotAnInteger:
        days = paginator.page(1)
    except EmptyPage:
        days = paginator.page(paginator.num_pages)

    enum = enumerate(paginator.object_list, 1)
    return [paginator, days, enum]



def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    day_form = DayForm()
    task_form = TaskForm()

    paginator, days, enum = pagination(request, slug)

    return render(request, 'project/detail.html', {'project': project,
                                                   'day_form': day_form,
                                                   'task_form': task_form,
                                                   'days': days,
                                                   'enum': enum})


def day_create(request, slug):
    project = get_object_or_404(Project, slug=slug)
    paginator, days, enum = pagination(request, slug)
    last_page = paginator.num_pages

    if request.POST:
        day_form = DayForm(request.POST)
        if day_form.is_valid():
            name = day_form.cleaned_data['name']
            day = Day(name=name, project=project)
            day.save()
            return redirect(reverse('project:project_detail', kwargs={'slug': slug}) + f'?page={last_page + 1}')
    else:
        day_form = DayForm()
        return render(request, 'day/create.html', {'day_form': day_form, 'project': project})

def day_delete(request, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    day.delete()
    return redirect(request.META.get('HTTP_REFERER'))

def task_create(request, slug, id):
    day = get_object_or_404(Day, id=id)
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            cd = task_form.cleaned_data
            name = cd['name']
            optional = cd['optional']
            task = Task(name=name, optional=optional, day=day)
            task.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        task_form = TaskForm()
        return render(request, 'includes/task/create.html', {'task_form': task_form,
                                                             'day': day,
                                                             'project': project})

def task_complete(request, slug, day_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = get_object_or_404(Project, slug=slug)
    day = get_object_or_404(Day, id=day_id)
    if request.POST:
        task.complete = request.POST.get('complete') == 'True'
        task.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'includes/task/complete.html',
                      {'task': task,
                       'project': project,
                       'day': day})


def task_delete(request, slug, day_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


# def task_edit(request, slug, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     if request.POST:
#         task.name = request.POST.get('name')
#         task.optional = request.POST.get('optional')
#         task.complete = request.POST.get('complete')
#         task.save()
#         return redirect('project:project_detail', slug=slug)
#     else:
#         tasks = Task.objects.all()
#         return render(request, 'includes/task/edit.html', {'tasks': tasks})


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
