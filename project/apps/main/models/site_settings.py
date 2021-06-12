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
    shop_address = models.CharField(max_length=300,verbose_name='Адрес магазина', default='')
    address_code_lat = models.CharField(max_length=200, verbose_name='Геометка, широта', default='59.225473')
    address_code_lon = models.CharField(max_length=200, verbose_name='Геометка, долгота', default='39.909615') 

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройка сайта"

    
    def __str__(self):
        return f'Настройки сайта {self.site_name}'


class MainSlider(models.Model):
    
    settings = models.ForeignKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name='slider'
    )
    postion = models.IntegerField(default=0, verbose_name='Позиция')
    image = models.ImageField(verbose_name='Картинка')
    title = models.CharField(max_length=200, null=True, verbose_name="Подпись")
    link = models.CharField(max_length=200, verbose_name='Ссылка', default='',)

    class Meta:
        verbose_name = 'Слайдер на главной старнице'
        verbose_name_plural = 'Слайдеры на главной странице'


class IndexCategories(models.Model):
    settings = models.ForeignKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name='index_categories'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='index_page',
        null=True,
        blank=True,
        verbose_name='Категория'
    )
    image = models.ImageField(verbose_name='Картинка')
    title = models.CharField(max_length=200, null=True, verbose_name='Подпись')

    class Meta:
        verbose_name = 'Категории на главной странице'
        verbose_name_plural = 'Категории на главной странице'
