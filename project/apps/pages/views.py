from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from apps.pages.models import Vacancy


# Create your views here.
class IndexView(TemplateView):
    template_name = 'pages/index.html'
    

class VacancyListView(ListView):
    model = Vacancy
    queryset = Vacancy.objects.all()
    template_name = 'pages/vacancy_list.html'


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'pages/vacancy.html'
