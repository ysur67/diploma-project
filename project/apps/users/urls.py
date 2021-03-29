from django.urls import path
from .views import RegistrationView, LoginView, ProfileView

app_name = 'account'
urlpatterns = [
    path('account/registration/', RegistrationView.as_view(), name='registration'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/profile', ProfileView.as_view(), name='profile'),
]
