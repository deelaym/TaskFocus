from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

FIELD_WIDTH = 42

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'style': f'width: {FIELD_WIDTH}%;'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'style': f'width: {FIELD_WIDTH}%;'}
    ))

class UserCreateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username', 'style': f'width: {FIELD_WIDTH}%;'}
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'style': f'width: {FIELD_WIDTH}%;'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password again', 'style': f'width: {FIELD_WIDTH}%;'}
    ))

