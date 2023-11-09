from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import LoginForm, UserCreateForm
from django.contrib import messages



class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'Your username and password didn\'t match.\nPlease try again.', extra_tags='danger')
        return super().form_invalid(form)

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

