from django import forms
from .models import Project, Day, Task


FIELD_WIDTH = 100

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': f'width: {FIELD_WIDTH}%;'}),
        }

class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': f'width: {FIELD_WIDTH}%;'}),
                  }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['day']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': f'width: {FIELD_WIDTH}%;', 'placeholder': 'Task'}),
            'optional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

