from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from .forms import LoginForm, UserCreateForm, CustomPasswordChangeForm, CustomPasswordResetForm
from django.contrib import messages
from django.contrib.auth.models import User


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'Your username and password didn\'t match.\nPlease try again.', extra_tags='danger')
        return super().form_invalid(form)

    def get_default_redirect_url(self):
        return f'/{self.request.user.username}/project/'


def register(request):
    if request.POST:
        form = UserCreateForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
        else:
            for field in form:
                messages.error(request, field.errors, extra_tags='danger')
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserCreateForm()
        return render(request, 'registration/register.html', {'form': form})


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm

    def form_invalid(self, form):
        for field in form:
            messages.error(self.request, field.errors, extra_tags='danger')
        return super().form_invalid(form)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    def form_invalid(self, form):
        for field in form:
            messages.error(self.request, field.errors, extra_tags='danger')
        return super().form_invalid(form)


def account_settings(request, username):
    return render(request, 'user/account_settings.html')


def account_delete(request, username):
    user = get_object_or_404(User, id=request.user.id)
    user.delete()
    return redirect('index')
