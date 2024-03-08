from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views import View

from .forms import SingInForm


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
        else:
            messages.error(request, 'Invalid username or password.')

        return HttpResponseRedirect(reverse('authentication:login'))  # Redirect back to login page

    def get(self, request):
        form = SingInForm()
        return render(request, 'authentication/login.html', {'form': form})


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect(reverse('authentication:login'))
