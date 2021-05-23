from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class FormMixin(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': "Логин"
            }),
        label="Ваш логин",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Пароль'
            }
        ),
        label="Пароль"
    )


class RegistrationForm(FormMixin):
    class Meta:
        model = User
        
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': "Ваш email"
            }),
        label="Почтовый адрес",
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Повторите пароль'
            }
        ),
        label="Подтверждение пароля")

    field_order = [
        'username',
        'email',
        'password',
        'password_confirmation'
    ]
        

class LoginForm(FormMixin):
    pass


class ChangeDataForm(forms.Form):
    email = forms.EmailField(
        label='Эл. адрес'
    )
    first_name = forms.CharField(
        label='Имя'
    )
    last_name = forms.CharField(
        label='Фамилия'
    )
