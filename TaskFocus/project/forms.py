from django import forms
from .models import Project, Day, Task


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 40rem;'}),
        }

class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['name', 'complete']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 40rem;'}),
                  }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['day']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 40rem;', 'placeholder': 'Task'}),
            'optional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

