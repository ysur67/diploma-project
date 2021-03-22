from django.db import models
from pytils.translit import slugify
import random
from django.db.models.signals import pre_init
from django.dispatch import receiver


class CatalogMixin(models.Model):
    id_1c = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Идентификатор из базы 1с"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Позиция активна",
        help_text="Оставить пустым, если позиция активна"
    )
    title = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=400,
        null=False,
        blank=False,
        unique=True,
        verbose_name='Слаг'
    )
    image = models.ImageField(
        null=True,
        blank=True,
        verbose_name='Картинка товара'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def set_slug(self):
        self.slug = slugify(self.title)

    def set_unique_slug(self):
        self.slug = slugify(self.title + str(random.randint(1, 10000)))


@receiver(pre_init, sender=CatalogMixin)
def instance_pre_init_receiver(sender, instance, **kwargs):
    if instance.title == '' or instance.title is None:
        instance.title = instance.id
        print(instance)
