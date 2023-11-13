import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Day, Task
from .forms import DayForm, TaskForm, ProjectForm
from django.contrib import messages
from django.http import JsonResponse
import json
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


DAY_WIDTH = 85


class ProjectList(LoginRequiredMixin, ListView):
    template_name = 'project/list.html'
    paginate_by = 5
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


@login_required
def project_create(request, username):
    if request.POST:
        project_form = ProjectForm(request.POST, user=request.user)
        if project_form.is_valid():
            cd = project_form.cleaned_data
            project = Project(name=cd['name'], user=request.user, color=cd['color'])
            project.save()
            return redirect('project:project_detail', username=request.user.username, slug=project.slug)
        else:
            for field in project_form:
                messages.error(request, field.errors, extra_tags='danger')
            return render(request, 'project/create.html', {'project_form': project_form})
    else:
        project_form = ProjectForm()
        return render(request, 'project/create.html', {'project_form': project_form})


@login_required
def project_edit(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
    if request.POST:
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            return redirect('project:project_detail', username=request.user.username, slug=slug)
        else:
            return render(request, 'project/edit.html', {'project_form': project_form,
                                                     'project': project})
    else:
        project_form = ProjectForm(instance=project)
        return render(request, 'project/edit.html', {'project_form': project_form,
                                                 'project': project})


@login_required
def project_edit_mode(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
    if request.POST:
        project.edit_mode = request.POST.get('edit_mode') == 'Edit mode on'
        project.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'includes/project/edit_mode.html', {'project': project})


@login_required
def project_delete(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
    project.delete()
    return redirect('project:project_list', username=request.user.username)


@login_required
def project_detail(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
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


@login_required
def project_restart(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
    for day in project.days.all():
        day.complete = False
        for task in day.tasks.all():
            task.complete = False
            task.save()
        day.save()
    if request.POST:
        project.complete = False
        project.save()
        return redirect('project:project_detail', username=request.user.username, slug=slug)
    return render(request, 'includes/project/restart.html', {'project': project})


@login_required
def project_timer(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
    current_time = project.timer
    if b'current_time' in request.body and b'duration' in request.body:
        data = json.loads(request.body)
        hours, minutes, seconds = map(int, data['current_time'].split(':'))
        project.timer = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

        date1, date2 = data['duration'][0], data['duration'][1]
        time1 = datetime.time(hour=date1[3], minute=date1[4], second=date1[5])
        time2 = datetime.time(hour=date2[3], minute=date2[4], second=date2[5])
        date1 = datetime.date(day=date1[0], month=date1[1], year=date1[2])
        date2 = datetime.date(day=date2[0], month=date2[1], year=date2[2])

        if date1 != date2:
            durations = {date1: [str(time1), str(datetime.time(hour=23, minute=59, second=59))],
                         date2: [str(datetime.time(hour=0, minute=0, second=0)), str(time2)]}
            project.time_periods.setdefault(str(date1), []).append(durations[date1])
            project.time_periods.setdefault(str(date2), []).append(durations[date2])
        else:
            durations = {date1: [str(time1), str(time2)]}
            project.time_intervals.setdefault(str(date1), []).append(durations[date1])
        project.save()
        return JsonResponse({'current_time': current_time, 'duration': data['duration']})

    return JsonResponse({'current_time': current_time})


@login_required
def project_set_dates(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
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


@login_required
def day_create(request, username, slug):
    project = get_object_or_404(Project, slug=slug, user=request.user.id)

    if request.POST:
        day_form = DayForm(request.POST)
        if day_form.is_valid():
            name = day_form.cleaned_data['name']
            day = Day(name=name, project=project)
            day.save()
            last_day_id = day.id
            return redirect('project:day_detail', username=request.user.username, slug=slug, day_id=last_day_id)
        else:
            return render(request, 'day/create.html', {'day_form': day_form, 'project': project})
    else:
        day_form = DayForm()
        return render(request, 'day/create.html', {'day_form': day_form, 'project': project})


@login_required
def day_detail(request, username, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug, user=request.user.id)

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


@login_required
def day_complete(request, username, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
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


@login_required
def day_edit(request, username, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug, user=request.user.id)

    if request.POST:
        day_form = DayForm(request.POST, instance=day)
        if day_form.is_valid():
            day_form.save()
            return redirect('project:day_detail', username=request.user.username, slug=slug, day_id=day_id)
        else:
            return render(request, 'day/edit.html', {'day_form': day_form,
                                                     'day': day,
                                                     'project': project})
    else:
        day_form = DayForm(instance=day)
        return render(request, 'day/edit.html', {'day_form': day_form,
                                                 'day': day,
                                                 'project': project})


@login_required
def day_delete(request, username, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    day.delete()
    return redirect('project:project_detail', username=request.user.username, slug=slug)


@login_required
def task_create(request, username, slug, day_id):
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
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


@login_required
def task_complete(request, username, slug, day_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    project = get_object_or_404(Project, slug=slug, user=request.user.id)
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


@login_required
def task_edit(request, username, slug, day_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    day = get_object_or_404(Day, id=day_id)
    project = get_object_or_404(Project, slug=slug, user=request.user.id)


    if request.POST:
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            return redirect('project:day_detail', username=request.user.username, slug=slug, day_id=day_id)
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


@login_required
def task_delete(request, username, slug, day_id, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def projects_reports(request, username):
    projects = Project.objects.filter(user=request.user.id)
    total_hours = sum([project.timer.total_seconds() for project in projects]) // 3600
    return render(request, 'project/reports.html', {'total_hours': total_hours})


@login_required
def projects_doughnut_chart(request, username):
    projects = Project.objects.filter(user=request.user.id)
    labels = [project.name for project in projects]
    data = [project.timer.total_seconds() // 3600 for project in projects]
    colors = [project.color for project in projects]
    projects = {'labels': labels, 'data': data, 'colors': colors}
    return JsonResponse(projects)
