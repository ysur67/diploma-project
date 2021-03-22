from django.urls import path
from .views import RegistrationView, LoginView

app_name = 'account'
urlpatterns = [
    path('account/registration/', RegistrationView.as_view(), name='registration'),
    path('account/login/', LoginView.as_view(), name='login'),
]
