from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
# from .models import AppUser
from django.views import View
from django.conf import settings as conf_settings
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from custom_auth.models import AppUser


class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect(reverse('posts:profile', args=(user.id,)))
        else:
            return render(request, 'posts/login.html', {})

    def post(self, request):
        body = request.POST
        username, password = body['username'], body['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username and/or password!")
            return render(request, 'posts/login.html',  {})
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('posts:profile', args=(user.id,)))


class RegisterView(View):
    def post(self, request):
        body = request.POST
        username, email, password = body['username'], body['email'], body['password']
        user = AppUser.objects.create_user(
            username, email, password, first_name=body['first_name'], last_name=body['last_name'])
        login(request, user)
        return HttpResponseRedirect(reverse('posts:profile', args=(user.id,)))


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('posts:login'))
