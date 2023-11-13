from django.db import models
from datetime import timedelta
from django.utils.text import slugify
from django.contrib.auth.models import User



class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=30)
    timer = models.DurationField(default=timedelta(seconds=0))
    time_intervals = models.JSONField(default=dict())
    slug = models.SlugField()
    edit_mode = models.BooleanField(default=True)
    complete = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#994299')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def timer_string(self):
        time = str(self.timer).replace(', ', ':').split(':')

        if len(time) == 4:
            time[0] = time[0].split()[0]
            time_string = f'{int(time[0]) * 24 + int(time[1])}:{time[2].zfill(2)}:{time[3].zfill(2)}'
        else:
            time_string = f'{time[0].zfill(2)}:{time[1].zfill(2)}:{time[2].zfill(2)}'
        return time_string


class Day(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='days')
    name = models.CharField(max_length=30, blank=True, default='Day')
    complete = models.BooleanField(default=False)
    date = models.DateField(blank=True, null=True)


class Task(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)



