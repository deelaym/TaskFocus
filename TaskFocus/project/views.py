import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Day, Task
from .forms import DayForm, TaskForm, ProjectForm
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.generic import ListView


DAY_WIDTH = 85


def index(request):
    return render(request, 'index.html')


class ProjectList(ListView):
    model = Project
    template_name = 'project/list.html'
    paginate_by = 5
    context_object_name = 'projects'



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


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    first_day = project.days.filter(complete=False).first()
    last_day = project.days.last()

    days = project.days.all()
    paginated_days = []

    for i, day in enumerate(days):
        if i % 7 == 0:
            paginated_days.append([])
        paginated_days[-1].append(day)
    range_paginated_days = range(len(paginated_days))

    all_days = project.days.count()
    complete_days = project.days.filter(complete=True).count()
    if all_days:
        progress = int(complete_days / all_days * 100)
    else:
        progress = 0

    return render(request, 'project/detail.html', {'project': project,
                                                   'day': first_day if first_day else last_day,
                                                   'days': days,
                                                   'paginated_days': paginated_days,
                                                   'range_paginated_days': range_paginated_days,
                                                   'progress': progress,
                                                   'DAY_WIDTH': DAY_WIDTH})

def project_restart(request, slug):
    project = get_object_or_404(Project, slug=slug)
    for day in project.days.all():
        day.complete = False
        for task in day.tasks.all():
            task.complete = False
            task.save()
        day.save()
    if request.POST:
        project.complete = False
        project.save()
        return redirect('project:project_detail', slug=slug)
    return render(request, 'includes/project/restart.html', {'project': project})

def project_timer(request, slug):
    project = get_object_or_404(Project, slug=slug)
    current_time = project.timer
    if b'current_time' in request.body:
        data = json.loads(request.body)
        hours, minutes, seconds = map(int, data['current_time'].split(':'))
        project.timer = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        project.save()
        return JsonResponse({'current_time': current_time})

    return JsonResponse({'current_time': current_time})

def project_set_dates(request, slug):
    project = get_object_or_404(Project, slug=slug)
    date = datetime.datetime.now()
    if request.POST:
        for day in project.days.filter(complete=False):
            day.date = date
            date += datetime.timedelta(days=1)
            day.save()
        messages.success(request, 'Dates set successfully.', extra_tags='success')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'includes/project/set_dates.html', {'project': project})


def day_create(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.POST:
        day_form = DayForm(request.POST)
        if day_form.is_valid():
            name = day_form.cleaned_data['name']
            day = Day(name=name, project=project)
            day.save()
            last_day_id = day.id
            return redirect('project:day_detail', slug=slug, day_id=last_day_id)
        else:
            return render(request, 'day/create.html', {'day_form': day_form, 'project': project})
    else:
        day_form = DayForm()
        return render(request, 'day/create.html', {'day_form': day_form, 'project': project})


def day_detail(request, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug)

    day_form = DayForm()
    task_form = TaskForm()

    days = project.days.all()
    paginated_days = []

    date = datetime.datetime.now()

    for i, d in enumerate(days):
        if i % 7 == 0:
            paginated_days.append([])
        paginated_days[-1].append(d)
    range_paginated_days = range(len(paginated_days))

    if project.days.count():
        progress = int(project.days.filter(complete=True).count() / project.days.all().count() * 100)
    else:
        progress = 0

    return render(request, 'day/detail.html', {'day': day,
                                               'project': project,
                                               'day_form': day_form,
                                               'task_form': task_form,
                                               'date': date,
                                               'days': days,
                                               'paginated_days': paginated_days,
                                               'range_paginated_days': range_paginated_days,
                                               'progress': progress,
                                               'DAY_WIDTH': DAY_WIDTH})



def day_complete(request, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug)
    if request.POST:
        tasks_mandatory = day.tasks.filter(optional=False)
        if tasks_mandatory.count() == tasks_mandatory.filter(complete=True).count():
            day.complete = request.POST.get('complete') == 'Complete'
            day.save()

            all_days = project.days.all().count()
            complete_days = project.days.filter(complete=True).count()
            if all_days == complete_days:
                project.complete = True
                project.save()
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

    if request.POST:
        day_form = DayForm(request.POST, instance=day)
        if day_form.is_valid():
            day_form.save()
            return redirect('project:day_detail', slug=slug, day_id=day_id)
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
    return redirect('project:project_detail', slug=slug)



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


    if request.POST:
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('project:day_detail', slug=slug, day_id=day_id)
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


