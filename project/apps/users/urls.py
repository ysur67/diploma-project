from django.urls import path
from .views import RegistrationView, LoginView, ProfileView
from django.contrib.auth.decorators import login_required

app_name = 'account'
urlpatterns = [
    path('account/registration/', RegistrationView.as_view(), name='registration'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/profile', login_required(ProfileView.as_view()), name='profile'),
]
