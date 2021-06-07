from django.urls import path
from .views import (
    RegistrationView, LoginView,
    ChangeDataView, LogoutView,
    OrderListView, ChangePasswordView
)
from django.contrib.auth.decorators import login_required

app_name = 'account'
urlpatterns = [
    path('account/registration/', RegistrationView.as_view(), name='registration'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/profile/', ChangeDataView.as_view(), name='profile'),
    path('account/orders/', OrderListView.as_view(), name='order_list'),
    path('account/changepassword/', ChangePasswordView.as_view(), name='change_password')
]
