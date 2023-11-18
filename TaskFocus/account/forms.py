import string

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
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
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'E-mail', 'style': f'width: {FIELD_WIDTH}%;'}
    ))

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


    def clean_username(self):
        username = self.cleaned_data['username']
        chars = string.ascii_letters + '_' + string.digits
        for ch in username:
            if ch not in chars:
                raise forms.ValidationError('The username should only contain Latin letters, numbers, and underscore _.')
        if username == 'admin':
            raise forms.ValidationError('admin cannot be a username')
        return username


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Old password', 'style': f'width: {FIELD_WIDTH}%;'}
    ))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password', 'style': f'width: {FIELD_WIDTH}%;'}
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password again', 'style': f'width: {FIELD_WIDTH}%;'}
    ))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 'style': f'width: {FIELD_WIDTH}%;'}
    ))


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password', 'style': f'width: {FIELD_WIDTH}%;'}
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New password again', 'style': f'width: {FIELD_WIDTH}%;'}
    ))
