from django.db import models
from datetime import timedelta


class Project(models.Model):
    name = models.CharField(max_length=30)
    timer = models.DurationField(default=timedelta(seconds=0))


class Day(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='days')
    name = models.CharField(max_length=30, blank=True, default='Day')
    complete = models.BooleanField(default=False)


class Task(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='tasks')
    name = models.TextField(blank=True)
    url = models.URLField(blank=True)
    complete = models.BooleanField(default=False)
    optional = models.BooleanField(default=False)

