from django.contrib import admin
from apps.pages.models import Vacancy, VacancyRequirement, VacancyCondition, VacancyTask


class TaskInline(admin.StackedInline):
    model = VacancyTask
    extra = 0

class RequirementInline(admin.StackedInline):
    model = VacancyRequirement
    extra = 0


class ConditionInline(admin.StackedInline):
    model = VacancyCondition
    extra = 0


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    inlines = [TaskInline, RequirementInline, ConditionInline]
