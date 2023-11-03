from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Day, Task
from .forms import DayForm, TaskForm, ProjectForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib import messages


DAY_WIDTH = 85


def index(request):
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


def project_edit_mode(request, slug):
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        project.edit_mode = request.POST.get('edit_mode') == 'Edit mode on'
        project.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'includes/project/edit_mode.html', {'project': project})


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

    progress = int(project.days.filter(complete=True).count() / project.days.all().count() * 100)

    return render(request, 'project/detail.html', {'project': project,
                                                   'day_form': day_form,
                                                   'task_form': task_form,
                                                   'days': days,
                                                   'enum': enum,
                                                   'progress': progress,
                                                   'DAY_WIDTH': DAY_WIDTH})


def day_create(request, slug):
    project = get_object_or_404(Project, slug=slug)
    paginator, *_ = pagination(request, slug)
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


def day_complete(request, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        tasks_mandatory = day.tasks.filter(optional=False)
        if tasks_mandatory.count() == tasks_mandatory.filter(complete=True).count():
            day.complete = request.POST.get('complete') == 'Complete'
            day.save()
        elif request.POST.get('complete') != 'Complete':
            day.complete = False
            day.save()
        else:
            messages.error(request, 'All required tasks must be completed to complete the day.', extra_tags='danger')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'includes/day/complete.html', {'day': day,
                                                              'project': project})


def day_edit(request, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug)
    page = request.GET.get('page')

    if request.POST:
        day_form = DayForm(request.POST, instance=day)
        if day_form.is_valid():
            day_form.save()
            return redirect(reverse('project:project_detail', kwargs={'slug': slug}) + f'?page={page}')
        else:
            return render(request, 'day/edit.html', {'day_form': day_form,
                                                     'day': day,
                                                     'project': project})
    else:
        day_form = DayForm(instance=day)
        return render(request, 'day/edit.html', {'day_form': day_form,
                                                 'day': day,
                                                 'project': project})


def day_delete(request, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    day.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def task_create(request, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
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


def task_edit(request, slug, day_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug)
    page = request.GET.get('page')

    if request.POST:
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect(reverse('project:project_detail', kwargs={'slug': slug}) + f'?page={page}')
        else:
            return render(request, 'task/edit.html', {'task_form': task_form,
                                                               'task': task,
                                                               'day': day,
                                                               'project': project})
    else:
        task_form = TaskForm(instance=task)
        return render(request, 'task/edit.html', {'task_form': task_form,
                                                           'task': task,
                                                           'day': day,
                                                           'project': project,
                                                  'DAY_WIDTH': DAY_WIDTH})


def task_delete(request, slug, day_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


