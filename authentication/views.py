from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, reverse, redirect
from django.utils.http import urlsafe_base64_encode
from django.views import View

from .forms import SingInForm


class LoginView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.employee.first():
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


def generate_password_reset_link(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return HttpResponseBadRequest("Invalid user ID")

    uidb64 = urlsafe_base64_encode(str(user.pk).encode())
    token = default_token_generator.make_token(user)

    reset_url = reverse('authentication:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
    reset_link = request.build_absolute_uri(reset_url)

    return reset_link
