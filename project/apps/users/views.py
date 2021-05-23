from apps.shop.models import Order
from django.shortcuts import redirect
# from apps.main.utils.validators import UserChangeDataValidator
from django.views import generic
from django.views.generic.base import TemplateView
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from apps.main.utils import UserRegistrationValidator, UserLoginValidator, UserChangeDataValidator, UserChangePasswordValidator



class AccountMixin(TemplateView):

    def render_to_response(self, context, **response_kwargs):
        if not self.request.user.is_authenticated:
            return redirect('/')
        return super().render_to_response(context, **response_kwargs)

class RegistrationView(TemplateView):
    template_name = 'users/registration.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegistrationForm()
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        post_data = post.copy()
        validator = UserRegistrationValidator(post_data)
        json_response = {
            'errors': False,
            'fields': None,
            'message': ''
        }
        if validator.has_errors:
            json_response['errors'] = True
            json_response['fields'] = validator.errors
            return JsonResponse(json_response)

        user = User.objects.create(
            username=post_data['username'],
            email=post_data['email']
        )
        user.set_password(post_data['password_confirmation'])
        user.save()
        json_response['redirect'] = reverse_lazy('account:login')
        return JsonResponse(json_response)


class LoginView(TemplateView):
    template_name = 'users/login.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        post = request.POST
        post_data = post.copy()
        validator = UserLoginValidator(post_data)
        json_response = {
            'errors': False,
            'fields': None,
            'redirect': ''
        }
        if validator.has_errors:
            json_response['errors'] = True
            json_response['fields'] = validator.errors
            return JsonResponse(json_response)

        user = authenticate(
            username=post_data['username'],
            password=post_data['password']
        )
        login(request, user)
        json_response['redirect'] = reverse_lazy('account:profile')
        return JsonResponse(json_response)


class ChangeDataView(AccountMixin):
    template_name = 'users/profile.html'

    def post(self, request, *args, **kwargs):
        post = request.POST
        post_data = post.copy()
        json_response = {
            'errors': False,
            'fields': None,
            'redirect': ''
        }
        validator = UserChangeDataValidator(post_data, request.user)
        if validator.has_errors:
            json_response['errors'] = True
            json_response['fields'] = validator.errors
            return JsonResponse(json_response)

        user = request.user
        user.username = post_data['username']
        user.first_name = post_data['first_name']
        user.last_name = post_data['last_name']
        user.email = post_data['email']
        user.save()
        json_response['username'] = user.username
        return JsonResponse(json_response)


class OrderListView(AccountMixin):
    template_name = 'users/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context


class ChangePasswordView(AccountMixin):
    template_name = 'users/change_password.html'

    def post(self, request, *args, **kwargs):
        post = request.POST
        post_data = post.copy()
        json_response = {
            'errors': False,
            'fields': None,
        }
        validator = UserChangePasswordValidator(post_data, request.user)
        if validator.has_errors:
            json_response['errors'] = True
            json_response['fields'] = validator.errors
            return JsonResponse(json_response)

        user = request.user
        user.set_password(post_data['password_confirmation'])
        user.save()
        login(request, user)
        return JsonResponse(json_response)


class UserLogoutView(LogoutView):
    pass


def user_exists(username: str, email: str) -> bool:
    """Checks if user is already in db

    If given only username, just paste empty string instead
    of user's email"""
    if User.objects.filter(username=username).exists()\
        or User.objects.filter(email=email).exists():

        return True
    else:
        return False

