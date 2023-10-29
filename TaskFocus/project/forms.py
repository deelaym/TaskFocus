from django import forms
from .models import Project, Day, Task


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 23rem;'}),
                  }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['day']
