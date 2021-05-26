from django.urls import path
from apps.pages.views import VacancyListView, VacancyDetailView

app_name='pages'
urlpatterns = [
    path('pages/vacancies/', VacancyListView.as_view(), name='vacancy_list'),
    path('pages/vacancies/<pk>', VacancyDetailView.as_view(), name='vacancy')
]
