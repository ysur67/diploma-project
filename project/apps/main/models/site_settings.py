from django.db import models

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
        verbose_name="Ссылка на главный сайт"
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон в футуре"
    )

    scripts = models.TextField(
        verbose_name="Скрипты в хедере"
    )
    seo_tags = models.CharField(
        max_length=100,
        verbose_name="Теги для сео"
    )

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"