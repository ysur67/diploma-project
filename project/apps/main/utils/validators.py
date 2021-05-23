from django.contrib import auth
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login

class Validator:
    def __init__(self, post_data):
        self._data = post_data
        self._fields = dict()
        self._clear_data()
        self._validate_fields()

    def _validate_fields(self):
        raise NotImplementedError('Has to be implemented')

    def _add_error(self, field_name, error_message):
        self._fields[field_name] = error_message

    @property
    def has_errors(self):
        if self._fields:
            return True

        return False

    @property
    def errors(self):
        return self._fields

    def _clear_data(self):
        for key in self._data:
            self._data[key] = str(self._data[key]).replace(' ', '')


class OrderFormValidator(Validator):

    def _validate_fields(self):
        self._validate_full_name()
        self._validate_phone()
        self._validate_email()
        return None

    def _validate_full_name(self):
        FIELD_NAME = 'full_name'
        name = self._data[FIELD_NAME]
        if not name:
            self._add_error(FIELD_NAME, 'ФИО не может быть пустым')


    def _validate_phone(self):
        FIELD_NAME = 'phone'
        phone = self._data[FIELD_NAME]
        if not phone:
            self._add_error(FIELD_NAME, 'Номер телефона не может быть пустым')

        LENGTH = 11
        FIRST_NUMS = (7, 8)
        clear_phone = re.sub('[^\d]', '', phone)
        if len(clear_phone) != LENGTH:
            self._add_error(FIELD_NAME, 'Неверная длина номера телефона')
            return

        elif int(clear_phone[0]) not in FIRST_NUMS:
            self._add_error(FIELD_NAME, 'Телефон не принадлежит российскому провайдеру')
            return

        return True

    def _validate_email(self):
        FIELD_NAME = 'email'
        email = self._data[FIELD_NAME]
        if not email:
            self._add_error(FIELD_NAME, 'Адрес эл. почты не может быть пустым')

        EMAIL_REGEX = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not re.search(EMAIL_REGEX, email):
            self._add_error(FIELD_NAME, 'Неверный адрес эл. почты')


class UserRegistrationValidator(Validator):
    
    def _validate_fields(self):
        self._validate_username()
        self._validate_email()
        self._validate_passwords()

    def _validate_username(self):
        FIELD_NAME = 'username'
        username = self._data.get(FIELD_NAME, None)
        if not username:
            self._add_error(FIELD_NAME, 'Имя пользователя не может быть пустым')
            return
        users = User.objects.filter(username=username)
        if users.exists():
            self._add_error(FIELD_NAME, 'Пользователь с таким именем уже существует')
            return
        if len(username) < 4:
            self._add_error(FIELD_NAME, 'Имя пользователя не может быть меньше 5 символов')
            

    def _validate_email(self):
        FIELD_NAME = 'email'
        email = self._data[FIELD_NAME]
        if not email:
            self._add_error(FIELD_NAME, 'Адрес эл. почты не может быть пустым')

        EMAIL_REGEX = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if not re.search(EMAIL_REGEX, email):
            self._add_error(FIELD_NAME, 'Неверный адрес эл. почты')

    def _validate_passwords(self):
        FIELD_NAME = 'password'
        FIELD_NAME_REPEAT = 'password_confirmation'

        pswd = self._data.get(FIELD_NAME, None)
        pswd_confirm = self._data.get(FIELD_NAME_REPEAT, None)

        if not pswd:
            self._add_error(FIELD_NAME, 'Пароль не может быть пустым')
            return

        if not pswd_confirm:
            self._add_error(FIELD_NAME_REPEAT, 'Повторите пароль')
            return

        if pswd != pswd_confirm:
            self._add_error(FIELD_NAME, 'Пароли не совпадают')
            self._add_error(FIELD_NAME_REPEAT, 'Пароли не совпадают')


class UserLoginValidator(Validator):
    def _validate_fields(self):
        self._vadlidate_username()
        self._validate_password()

    def _vadlidate_username(self):
        FIELD_NAME = 'username'
        username = self._data.get(FIELD_NAME, None)

        if not username:
            self._add_error(FIELD_NAME, 'Имя пользователя не может быть пустым')
            return

        user_list = User.objects.filter(username=username)
        if not user_list.exists():
            self._add_error(FIELD_NAME, 'Пользователя с указанным логином не существует')

        if user_list.count() > 1:
            self._add_error(FIELD_NAME, 'Несколько пользователей с указанным логином, свяжитесь с администрацией')


    def _validate_password(self):
        FIELD_NAME = 'password'
        pswd = self._data.get(FIELD_NAME, None)

        if not pswd:
            self._add_error(FIELD_NAME, 'Пароль не может быть пустым')
            return

        username = self._data.get('username', '')
        user = authenticate(username=username, password=pswd)
        if not user:
            self._add_error(FIELD_NAME, 'Проверьте введенные данные')


class UserChangeDataValidator(Validator):
    
    def __init__(self, post_data, user):
        self._user = user
        super().__init__(post_data)

    def _validate_fields(self):
        self._validate_username()
        self._validate_email()

    def _validate_username(self):
        FIELD_NAME = 'username'
        username = self._data.get(FIELD_NAME, None)

        if not username:
            self._add_error(FIELD_NAME, 'Имя пользователя не может быть пустым')
            return

        user_list = User.objects.filter(username=username).exclude(id=self._user.id)
        if user_list.exists():
            self._add_error(FIELD_NAME, 'Имя пользователя уже занято')

    def _validate_email(self):
        FIELD_NAME = 'email'
        email = self._data.get(FIELD_NAME, None)
        if not email:
            self._add_error(FIELD_NAME, 'Эл. почта не может быть пустой')
            return

        user_list = User.objects.filter(email=email).exclude(id=self._user.id)
        if user_list.exists():
            self._add_error(FIELD_NAME, 'Адрес эл. почты уже занят')


class UserChangePasswordValidator(Validator):
    def __init__(self, post_data, user):
        self._user = user
        super().__init__(post_data)

    def _validate_fields(self):
        self._validate_old_password()
        self._validate_passwords()

    def _validate_old_password(self):
        FIELD_NAME = 'old_password'
        old_pswd = self._data.get(FIELD_NAME, '')
        old_pswd = old_pswd.replace(' ', '')
        if not self._user.check_password(old_pswd):
            self._add_error(FIELD_NAME, 'Неверный старый пароль')


    def _validate_passwords(self):
        FIELD_NAME = 'password'
        FIELD_NAME_REPEAT = 'password_confirmation'

        pswd = self._data.get(FIELD_NAME, None)
        pswd_confirm = self._data.get(FIELD_NAME_REPEAT, None)

        if not pswd:
            self._add_error(FIELD_NAME, 'Пароль не может быть пустым')
            return

        if not pswd_confirm:
            self._add_error(FIELD_NAME_REPEAT, 'Повторите пароль')
            return

        if pswd != pswd_confirm:
            self._add_error(FIELD_NAME, 'Пароли не совпадают')
            self._add_error(FIELD_NAME_REPEAT, 'Пароли не совпадают')
