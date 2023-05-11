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
from users.models import AppUser
from django.db import IntegrityError
from django.http import JsonResponse


class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return HttpResponseRedirect(reverse('main:main', args=(user.id,)))
        else:
            return render(request, 'users/login.html', {})

    def post(self, request):
        body = request.POST
        username, password = body['username'], body['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username and/or password!")
            return render(request, 'users/login.html',  {})
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('main:main', args=(user.id,)))


class RegisterView(View):
    def post(self, request):
        body = request.POST
        print(request.POST)
        username, email, password = body['username'], body['email'], body['password']
        try:
            user = AppUser.objects.create_user(
                username, email, password, first_name=body['first_name'], last_name=body['last_name'])
        except IntegrityError as e:
            return JsonResponse({'error': 'Username already exists.'})

        login(request, user)
        return JsonResponse({'url': reverse('main:main', args=(user.id,))})


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('users:login'))


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        q = request.GET.get('q')
        return JsonResponse({'user_list': q})


class ProfilePictureView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        user.profile_picture = request.FILES['image']
        user.save()
        return JsonResponse({'url': user.get_profile_picture_round()})


class CoverPhotoView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        user.cover_photo = request.FILES['image']
        user.save()
        return JsonResponse({'url': user.get_cover_photo()})
