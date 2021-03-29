from django.shortcuts import render
from django.views import generic
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login


class RegistrationView(generic.FormView):
    form_class = RegistrationForm
    success_url = reverse_lazy('catalog:category_list')
    template_name = 'users/registration.html'

    def form_valid(self, form):
        email = form.cleaned_data['username']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        password_confirmation = form.cleaned_data['password_confirmation']
        if not user_exists(username, email) \
            and password_confirmation == password:
            user = User.objects.create(
                username=username,
                email=email)
            user.set_password(password_confirmation)
            user.save()
            return JsonResponse({
                'errors': False,
                'message': 'Пользователь успешно создан!',
                'redirect': reverse_lazy('catalog:category_list')
            })
        elif password != password_confirmation:
            return JsonResponse({
                'errors': True,
                'message': 'Пароли не совпадают'
            })
        else:
            return JsonResponse({
                'errors': True,
                'message': 'Пользователь с таким логином уже зарегестрирован'
            })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': True,
            'fields': form.errors
        })


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        users = User.objects.all()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(
            username=username,
            password=password)
        print(user)
        if user:
            login(
                self.request,
                user=user)
            return JsonResponse({
                'errors': False,
                'redirect': reverse_lazy('catalog:category_list') 
            })
        else:
            if user_exists(username, ''):
                return JsonResponse({
                    'errors': True,
                    'message': 'Ваш пароль не верен!!'
                })
            else:
                return JsonResponse({
                    'errors': True,
                    'message': 'Пользователя с указанным логином \
                        не существует!'
                })

    def form_invalid(self, form):
        return JsonResponse({
            'errors': True,
            'fields': form.errors
        })


class ProfileView(generic.TemplateView):
    template_name = 'users/profile.html'

def user_exists(username: str, email: str) -> bool:
    """Checks if user is already in db

    If given only username, just paste empty string instead
    of user's email"""
    if User.objects.filter(username=username).exists()\
        or User.objects.filter(email=email).exists():

        return True
    else:
        return False
