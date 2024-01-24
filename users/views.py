from django.shortcuts import render, HttpResponseRedirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Users
from django.shortcuts import get_object_or_404


@login_required
def profile(request):
    user_id = request.user.id
    queryset = Users.objects.get(id=user_id)  # get_object_or_404(Account, pk=user_id)
    return render(request, 'users/profile.html', {'profile': queryset})


def register(request):
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('успешная регистрация'))
            return HttpResponseRedirect('../../')
        else:
            return render(request, 'users/register.html', {'form': form})


class BBLoginView(LoginView):
    template_name = 'users/login.html'


class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'
