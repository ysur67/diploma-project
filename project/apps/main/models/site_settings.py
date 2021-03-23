from django.db import models
from apps.catalog.models import Category


class SiteSettings(models.Model):
    
    site_name = models.CharField(
        null=False,
        blank=False,
        max_length=200,
    )
    favicon = models.ImageField(
        null=False,
        blank=False,
    )
    vk = models.CharField(
        max_length=300,
        verbose_name="Ссылка на группу вк"
    )
    instagram = models.CharField(
        max_length=300,
        verbose_name="Ссылка на профиль в инстраграм"
    )
    main_site = models.CharField(
        max_length=300,
        verbose_name="Ссылка на главный сайт",
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон в футуре",
        null=True,
        blank=True,
    )

    scripts = models.TextField(
        verbose_name="Скрипты в хедере",
        null=True,
        blank=True,
    )
    seo_tags = models.CharField(
        max_length=100,
        verbose_name="Теги для сео",
        null=True,
        blank=True,
    )
    header_categories = models.ManyToManyField(
        Category,
        related_name='header_display',
        blank=True,
        verbose_name='Категории в меню навигации'
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройка сайта"

    
    def __str__(self):
        return f'Настройки сайта {self.site_name}'
