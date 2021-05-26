from django.db import models
from ckeditor.fields import RichTextField


class Vacancy(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    description = RichTextField(verbose_name='Описание вакансии')
    show_salary = models.BooleanField(default=False, verbose_name='Показывать зарплату')
    salary_start = models.DecimalField(
        null=True,
        blank=True,
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='Минимальная зарплата'
    )
    salary_end = models.DecimalField(
        null=True,
        blank=True,
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='Максимальная зарплата'
    )
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self) -> str:
        return self.title


class VacancyTask(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        related_name='tasks',
        verbose_name='Задачи для соискателя',
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name='Описание задачи')

    class Meta:
        verbose_name = 'Задача для соискателя'
        verbose_name_plural = 'Задачи для соискателя'


class VacancyRequirement(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        related_name='requirements',
        verbose_name='Требования к соискателю',
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name='Описание требования')

    class Meta:
        verbose_name = 'Требование к соискателю'
        verbose_name_plural = 'Требования к соискателю'


class VacancyCondition(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        related_name='conditions',
        verbose_name='Условия работы для соискателя',
        on_delete=models.CASCADE
    )
    text = models.TextField(verbose_name='Описание условия труда')

    class Meta:
        verbose_name = 'Условие работы для соискателя'
        verbose_name_plural = 'Условия работы для соискателя'
