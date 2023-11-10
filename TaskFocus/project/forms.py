from django import forms
from .models import Project, Day, Task


FIELD_WIDTH = 100
TASK_FIELD_WIDTH = 90

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': f'width: {FIELD_WIDTH}%;'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Project.objects.filter(name=name, user=self.user).exists():
            raise forms.ValidationError('A project with the same name already exists.')
        return name



class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['name', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': f'width: {FIELD_WIDTH}%;'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
                  }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ['day']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': f'width: {TASK_FIELD_WIDTH}%;', 'placeholder': 'Task'}),
            'optional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

