from django.urls import path
from apps.pages import views


app_name = 'pages'
urlpatterns = [
    path('suka/', views.IndexView.as_view(), name='index'),
]
